import unittest
import urllib.error

from lib.http import HttpPolicy, HttpResponse, classify_exception, fetch_pdf
from tests.helpers import HTML_NO_LINK, HTML_WITH_LINK, PDF_BYTES, http_error, http_fake_factory, pdf_response, ssl_error


def policy(**over) -> HttpPolicy:
    base = dict(user_agent="spr/1.1 (mailto:{email})", alt_user_agent="Mozilla/5.0 test", contact_email="t@example.org", timeout=5)
    base.update(over)
    return HttpPolicy(**base)


class FetchPdfTests(unittest.TestCase):
    def test_plain_pdf(self):
        http = http_fake_factory([(r"paper\.pdf", pdf_response("https://x/paper.pdf"))])
        res = fetch_pdf("https://x/paper.pdf", policy(), http)
        self.assertTrue(res.ok)
        self.assertEqual(res.data, PDF_BYTES)
        self.assertEqual(http.calls[0][1], "spr/1.1 (mailto:t@example.org)")

    def test_403_retries_with_alt_ua_once(self):
        def responder(url, headers, verify_ssl):
            if headers["User-Agent"].startswith("Mozilla"):
                return pdf_response(url)
            return http_error(url, 403)

        http = http_fake_factory([(r"x/", responder)])
        res = fetch_pdf("https://x/p.pdf", policy(), http)
        self.assertTrue(res.ok)
        self.assertEqual([c[1] for c in http.calls], ["spr/1.1 (mailto:t@example.org)", "Mozilla/5.0 test"])

    def test_403_twice_is_blocked(self):
        http = http_fake_factory([(r"x/", http_error("u", 403))])
        res = fetch_pdf("https://x/p.pdf", policy(), http)
        self.assertFalse(res.ok)
        self.assertEqual(res.error_class, "blocked_403")
        self.assertEqual(len(http.calls), 2)

    def test_403_no_retry_when_disabled(self):
        http = http_fake_factory([(r"x/", http_error("u", 403))])
        res = fetch_pdf("https://x/p.pdf", policy(retry_alt_ua_on_403=False), http)
        self.assertEqual(res.error_class, "blocked_403")
        self.assertEqual(len(http.calls), 1)

    def test_impersonation_after_two_403s(self):
        http = http_fake_factory([(r"x/", http_error("u", 403))])
        curl = http_fake_factory([(r"x/", pdf_response("https://x/p.pdf"))])
        res = fetch_pdf("https://x/p.pdf", policy(), http, curl_get=curl)
        self.assertTrue(res.ok)
        self.assertEqual(res.warnings, ["impersonated_client"])
        self.assertEqual(len(http.calls), 2)
        self.assertEqual(len(curl.calls), 1)

    def test_impersonation_disabled_or_unavailable(self):
        http = http_fake_factory([(r"x/", http_error("u", 403))])
        curl = http_fake_factory([(r"x/", pdf_response("https://x/p.pdf"))])
        res = fetch_pdf("https://x/p.pdf", policy(impersonate_on_403=False), http, curl_get=curl)
        self.assertEqual(res.error_class, "blocked_403")
        self.assertEqual(len(curl.calls), 0)
        res = fetch_pdf("https://x/p.pdf", policy(), http)  # fake transport, no curl_get -> never impersonates
        self.assertEqual(res.error_class, "blocked_403")

    def test_ssl_retry_unverified(self):
        def responder(url, headers, verify_ssl):
            return pdf_response(url) if not verify_ssl else ssl_error()

        http = http_fake_factory([(r"x/", responder)])
        res = fetch_pdf("https://x/p.pdf", policy(), http)
        self.assertTrue(res.ok)
        self.assertEqual(res.warnings, ["ssl_unverified"])
        self.assertEqual([c[2] for c in http.calls], [True, False])

    def test_ssl_retry_disabled(self):
        http = http_fake_factory([(r"x/", ssl_error())])
        res = fetch_pdf("https://x/p.pdf", policy(ssl_retry_unverified=False), http)
        self.assertFalse(res.ok)
        self.assertEqual(res.error_class, "ssl_error")
        self.assertEqual(res.warnings, [])
        self.assertEqual(len(http.calls), 1)

    def test_html_follows_citation_pdf_url(self):
        http = http_fake_factory([
            (r"landing", HttpResponse(200, HTML_WITH_LINK, "text/html", "https://x/landing")),
            (r"from-html\.pdf", pdf_response("https://example.org/pdf/from-html.pdf")),
        ])
        res = fetch_pdf("https://x/landing", policy(), http)
        self.assertTrue(res.ok)
        self.assertEqual(http.calls[1][0], "https://example.org/pdf/from-html.pdf")

    def test_small_challenge_page_is_blocked_challenge(self):
        page = b'<!DOCTYPE html><html><head><title>&nbsp;</title></head><body><div id="challenge">Please verify you are human</div></body></html>'
        http = http_fake_factory([(r"mdpi", HttpResponse(200, page, "text/html", "https://www.mdpi.com/x/pdf"))])
        res = fetch_pdf("https://www.mdpi.com/x/pdf", policy(), http)
        self.assertFalse(res.ok)
        self.assertEqual(res.error_class, "blocked_challenge")
        self.assertEqual(res.error, "js_challenge_page")

    def test_large_page_with_marker_word_still_follows_link(self):
        page = (b'<html><head><meta name="citation_pdf_url" content="https://example.org/pdf/from-html.pdf"></head>'
                b"<body>please verify your email " + b"x" * 30000 + b"</body></html>")
        http = http_fake_factory([(r"landing", HttpResponse(200, page, "text/html", "https://x/landing")),
                                  (r"from-html\.pdf", pdf_response("https://example.org/pdf/from-html.pdf"))])
        self.assertTrue(fetch_pdf("https://x/landing", policy(), http).ok)

    def test_html_without_link_is_invalid_pdf(self):
        http = http_fake_factory([(r"landing", HttpResponse(200, HTML_NO_LINK, "text/html", "https://x/landing"))])
        res = fetch_pdf("https://x/landing", policy(), http)
        self.assertFalse(res.ok)
        self.assertEqual(res.error_class, "invalid_pdf")
        self.assertEqual(res.error, "html_without_pdf_link")

    def test_classify_exception(self):
        self.assertEqual(classify_exception(http_error("u", 403))[0], "blocked_403")
        self.assertEqual(classify_exception(http_error("u", 404))[0], "not_found")
        self.assertEqual(classify_exception(http_error("u", 500))[0], "network")
        self.assertEqual(classify_exception(ssl_error())[0], "ssl_error")
        self.assertEqual(classify_exception(urllib.error.URLError("timed out"))[0], "network")


if __name__ == "__main__":
    unittest.main()
