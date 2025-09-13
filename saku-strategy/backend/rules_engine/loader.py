import os
import yaml
from pathlib import Path
from typing import Any, Dict


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_rules() -> Dict[str, Any]:
    rules_path = project_root() / 'rules' / 'rules.yaml'
    if not rules_path.exists():
        return {}
    with open(rules_path) as f:
        return yaml.safe_load(f) or {}



