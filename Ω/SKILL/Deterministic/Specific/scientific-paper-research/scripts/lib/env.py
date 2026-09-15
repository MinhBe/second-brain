"""Environment lookup with a Windows registry fallback (User, then Machine level).

`setx NAME value` writes HKCU\\Environment; a shell opened before that, or a tool that
spawns Python without a login shell, will not see it in os.environ. This fills the gap.
"""

import sys
from typing import Any, Callable, Dict, Optional

NAMES = ("UNPAYWALL_EMAIL", "ELSEVIER_API_KEY")


def _registry_lookup(name: str) -> Optional[str]:
    if sys.platform != "win32":
        return None
    try:
        import winreg
    except ImportError:
        return None
    for hive, path in (
        (winreg.HKEY_CURRENT_USER, r"Environment"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
    ):
        try:
            with winreg.OpenKey(hive, path) as key:
                value, _ = winreg.QueryValueEx(key, name)
        except OSError:
            continue
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def resolve_env(name: str, env: Dict[str, Any], registry: Callable[[str], Optional[str]] = _registry_lookup) -> Optional[str]:
    value = env.get(name)
    if value:
        return str(value)
    return registry(name)


def resolved_env(env: Dict[str, Any], registry: Callable[[str], Optional[str]] = _registry_lookup) -> Dict[str, Any]:
    """Copy of env where every name in NAMES is filled from the registry when missing."""
    out = dict(env)
    for name in NAMES:
        if not out.get(name):
            value = registry(name)
            if value:
                out[name] = value
    return out
