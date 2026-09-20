# BROWSER RECOVERY TESTS (MILESTONE 2)

## 1. Fault Scenarios & Automated Recovery Matrix
| Scenario ID | Fault Injected | Observed Behavior | Recovery Mechanism | Verdict |
|---|---|---|---|---|
| **REC-001** | Profile Lock Contention (2 workers requesting Profile 1) | Second worker receives immediate non-blocking timeout | Second worker enters exponential backoff wait or routes to alternative worker without crashing | **PASSED** |
| **REC-002** | Network Timeout / Tab Unresponsive | Web page fails to return completion token within deadline | System flags session as `status: interrupted`, logs partial response, releases lock cleanly | **PASSED** |
| **REC-003** | Owner Interactive Session Protection | Owner is actively browsing on Chrome window | Agent respects existing session; uses non-disruptive accessibility hooks or separate data directory; never terminates user tabs | **PASSED** |
| **REC-004** | Provider Rate Limiting | External service returns rate limit or quota notice | Interceptor records `last_used_at` and `retry_after`, suppresses further calls, alerts Laura | **PASSED** |

## 2. Integrity Guarantee
No browser error or connection interruption causes data loss, orphan lock files (due to 300s TTL auto-expiry), or user browser tab disruption.
