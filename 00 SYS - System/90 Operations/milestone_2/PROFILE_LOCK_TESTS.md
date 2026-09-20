# PROFILE LOCK TESTS (MILESTONE 2)

## 1. Concurrency Safety Model
- **Lock Target**: Mutex file-based locking at `%LOCALAPPDATA%\hermes\locks\profile_<id>.lock`.
- **TTL & Deadlock Protection**: 300-second maximum lock TTL automatically clears orphaned locks if a worker crashes.
- **Mutual Exclusion**: Ensures that only one worker can control a specific Chrome profile at any time.

## 2. Test Execution & Evidence
- **Scenario**: 2 competing workers (`TASK_ALPHA_001` and `TASK_BETA_002`) requested access to `Profile 1`.
- **Step 1**: `TASK_ALPHA_001` acquired lock: `True` (Lock acquired for Profile 1 by task TASK_ALPHA_001).
- **Step 2**: `TASK_BETA_002` attempted to acquire lock while held by `TASK_ALPHA_001`: Correctly rejected with timeout `False` (Timeout acquiring lock for Profile 1 (held by other task)).
- **Step 3**: `TASK_ALPHA_001` released lock: `True` (Lock released for Profile 1 by task TASK_ALPHA_001).
- **Step 4**: `TASK_BETA_002` successfully acquired lock once freed: `True` (Lock acquired for Profile 1 by task TASK_BETA_002).

## 3. Verification Status
**PASSED**. Mutex locking functions reliably, preventing resource conflicts across Chrome profiles.
