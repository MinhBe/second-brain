import unittest

from lib.env import _registry_lookup, resolve_env, resolved_env


def fake_registry(values):
    return lambda name: values.get(name)


class EnvTests(unittest.TestCase):
    def test_process_env_wins(self):
        self.assertEqual(resolve_env("UNPAYWALL_EMAIL", {"UNPAYWALL_EMAIL": "a@x"}, fake_registry({"UNPAYWALL_EMAIL": "b@x"})), "a@x")

    def test_registry_fallback(self):
        self.assertEqual(resolve_env("UNPAYWALL_EMAIL", {}, fake_registry({"UNPAYWALL_EMAIL": "b@x"})), "b@x")
        self.assertIsNone(resolve_env("UNPAYWALL_EMAIL", {"UNPAYWALL_EMAIL": ""}, fake_registry({})))

    def test_resolved_env_fills_only_missing_names(self):
        out = resolved_env({"ELSEVIER_API_KEY": "k", "OTHER": "o"}, fake_registry({"UNPAYWALL_EMAIL": "b@x", "ELSEVIER_API_KEY": "reg"}))
        self.assertEqual(out, {"ELSEVIER_API_KEY": "k", "OTHER": "o", "UNPAYWALL_EMAIL": "b@x"})

    def test_real_registry_lookup_never_raises(self):
        self.assertIsNone(_registry_lookup("SPR_TEST_NAME_THAT_DOES_NOT_EXIST"))


if __name__ == "__main__":
    unittest.main()
