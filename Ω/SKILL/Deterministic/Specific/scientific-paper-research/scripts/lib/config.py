"""Config/schema loaders. All paths resolve relative to the skill root."""

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

SKILL_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = SKILL_ROOT / "config"
SCHEMA_DIR = SKILL_ROOT / "schemas"
REFERENCES_DIR = SKILL_ROOT / "references"
CONTRACT_VERSION = "1.3"


@lru_cache(maxsize=None)
def load_yaml(name: str) -> Dict[str, Any]:
    import yaml  # imported lazily so run.py can report missing_dependency

    path = CONFIG_DIR / f"{name}.yaml"
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


@lru_cache(maxsize=None)
def load_schema(name: str) -> Dict[str, Any]:
    path = SCHEMA_DIR / f"{name}.schema.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
