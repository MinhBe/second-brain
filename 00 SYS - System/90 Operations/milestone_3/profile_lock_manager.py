#!/usr/bin/env python3
"""
Enhanced Profile Lock Manager for Hermes AI Browser Gateway
Supports Mutex Locking, Heartbeat / Lease Extension, and Deadlock TTL Protection.
"""
import os
import time
import json

LOCKS_DIR = os.path.expandvars(r"%LOCALAPPDATA%\hermes\locks")
os.makedirs(LOCKS_DIR, exist_ok=True)

class ProfileLockManager:
    def __init__(self, locks_dir=None, default_ttl=300):
        self.locks_dir = locks_dir or LOCKS_DIR
        self.default_ttl = default_ttl

    def _get_lock_file(self, profile_id):
        safe_name = profile_id.replace(" ", "_").lower()
        return os.path.join(self.locks_dir, f"profile_{safe_name}.lock")

    def is_locked(self, profile_id):
        lf = self._get_lock_file(profile_id)
        if not os.path.exists(lf):
            return False
        try:
            with open(lf, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Check timeout TTL
            if time.time() - data.get("timestamp", 0) > data.get("ttl", self.default_ttl):
                os.remove(lf)
                return False
            return True
        except:
            return False

    def acquire(self, profile_id, task_id, timeout_s=5, ttl=300, poll_interval=0.2):
        lf = self._get_lock_file(profile_id)
        start_time = time.time()
        while time.time() - start_time < timeout_s:
            if not self.is_locked(profile_id):
                try:
                    lock_data = {
                        "profile_id": profile_id,
                        "task_id": task_id,
                        "timestamp": time.time(),
                        "ttl": ttl,
                        "pid": os.getpid()
                    }
                    with open(lf, "w", encoding="utf-8") as f:
                        json.dump(lock_data, f)
                    return True, f"Lock acquired for {profile_id} by task {task_id}"
                except Exception as e:
                    pass
            time.sleep(poll_interval)
        return False, f"Timeout acquiring lock for {profile_id} (held by other task)"

    def renew_lease(self, profile_id, task_id, extend_seconds=120):
        """Heartbeat mechanism for long-running browser tasks."""
        lf = self._get_lock_file(profile_id)
        if not os.path.exists(lf):
            return False, "Cannot renew lease: lock file does not exist"
        try:
            with open(lf, "r+", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("task_id") == task_id:
                    data["timestamp"] = time.time()
                    data["ttl"] += extend_seconds
                    f.seek(0)
                    json.dump(data, f)
                    f.truncate()
                    return True, f"Heartbeat received: Lease extended for {profile_id} by {extend_seconds}s"
                else:
                    return False, f"Cannot renew: owned by {data.get('task_id')}, not {task_id}"
        except Exception as e:
            return False, str(e)

    def release(self, profile_id, task_id):
        lf = self._get_lock_file(profile_id)
        if not os.path.exists(lf):
            return True, "Lock file does not exist"
        try:
            with open(lf, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("task_id") == task_id:
                os.remove(lf)
                return True, f"Lock released for {profile_id} by task {task_id}"
            else:
                return False, f"Cannot release lock: owned by task {data.get('task_id')}, not {task_id}"
        except Exception as e:
            return False, str(e)
