# BÁO CÁO TÌNH HUỐNG — 8 BÀI CHƯA TẢI ĐƯỢC
> Ngày: 2026-09-11 | Tổng: 15/23 thành công | Còn lại: 8 bài

---

## PHÂN LOẠI

| Nhóm | Số bài | Mô tả |
|---|---|---|
| **A. CERN Handle.net 403** | 2 | CDN chặn IP datacenter, curl_cffi vẫn bị block |
| **B. MDPI html_without_pdf_link** | 3 | Impersonate pass 403, nhưng MDPI trả HTML không link PDF |
| **C. Subscription-only** | 3 | Không có OA ở bất kỳ nguồn nào |

---

## NHÓM A — CERN Handle.net (2 bài)

Lỗi: `http_403` trên `hdl.handle.net` — CDN CERN chặn IP datacenter, cả `curl_cffi` impersonate cũng không qua được.

| # | DOI | Tên bài | Publisher | manual_urls |
|---|---|---|---|---|
| 1 | `10.1007/978-3-031-76459-2_3` | ModSec-Learn: Boosting ModSecurity with Machine Learning | Springer | [hdl:11584/440487](https://hdl.handle.net/11584/440487), [hdl:11567/1259116](https://hdl.handle.net/11567/1259116), [hdl:11573/1753448](https://hdl.handle.net/11573/1753448) |
| 2 | `10.1109/TIFS.2025.3583234` | ModSec-AdvLearn: Countering Adversarial SQL Injections With Robust ML | IEEE TIFS | [hdl:11584/448666](https://hdl.handle.net/11584/448666), [hdl:11567/1291939](https://hdl.handle.net/11567/1291939) |

**Gợi ý:** Download thủ công từ trình duyệt cá nhân (không qua datacenter).

---

## NHÓM B — MDPI html_without_pdf_link (3 bài)

Lỗi: `impersonated_client` nhưng MDPI trả HTML trang article, không extract được link PDF trực tiếp. URL `...pdf?version=...` redirect về HTML.

| # | DOI | Tên bài | Journal | manual_urls |
|---|---|---|---|---|
| 3 | `10.3390/computers15060368` | Deployment-Oriented Multi-Embedding ML Framework for SQL Injection Detection | Computers 15(6) | [doi](https://doi.org/10.3390/computers15060368), [doaj](https://doaj.org/article/b9172caa127a447bb469de2e2b4a043a) |
| 4 | `10.3390/fi17010008` | GenSQLi: A Generative AI Framework for Automatically Securing WAFs Against SQLi | Future Internet 17(1) | [doi](https://doi.org/10.3390/fi17010008), [mdpi](https://www.mdpi.com/1999-5903/17/1/8/), [doaj](https://doaj.org/article/a70d313adcea411eae02140e8f1e24d7) |
| 5 | `10.3390/jcp2040039` | Detection of SQL Injection Attack Using ML Techniques: A Systematic Literature Review | J. Cybersecur. & Privacy 2(4) | [doi](https://doi.org/10.3390/jcp2040039), [doaj](https://doaj.org/article/b91628631abd42d7a451a37e33f5a934) |

**Gợi ý:** MDPI yêu cầu browser để lấy PDF — download thủ công hoặc bổ sung MDPI-specific extractor (tìm `?download=1` param).

---

## NHÓM C — Subscription-only (3 bài)

Không có link OA, không trên Sci-Hub. Đây là papers chỉ có thể truy cập qua institutional access.

| # | DOI | Tên bài | Publisher | Ghi chú |
|---|---|---|---|---|
| 6 | `10.1109/ICASSP55912.2026.11460610` | Multi-Agent Honeypot-Based Request-Response Context Dataset for Improved SQL Injection Detection | IEEE (ICASSP 2026) | Conference proceedings, chưa indexed |
| 7 | `10.1016/j.cose.2022.103054` | Synthetic attack data generation model applying GAN for intrusion detection | Elsevier (Computers & Security) | Elsevier subscription |
| 8 | `10.1007/s00779-019-01332-y` | GAN-based imbalanced data intrusion detection system | Springer (Personal & Ubiquitous Computing) | Springer subscription |

**Gợi ý:** Yêu cầu institutional access, liên hệ authors qua ResearchGate, hoặc tìm preprint trên arXiv/ResearchGate.

---

## TỔNG KẾT

| | Thành công | Thất bại |
|---|---|---|
| Trước chạy lại | 13 | 10 |
| Sau chạy lại | **15** (+2) | **8** (-2) |
| Tỷ lệ | **65.2%** | 34.8% |

**2 bài phục hồi thành công:**
- `10.1109/ACCESS.2023.3296707` (GAN Survey) — via `candidate_rewrites` (IEEE stampPDF) + figshare expander
- `10.1109/e-Science62913.2024.10678662` (West et al.) — via scihub_fallback
