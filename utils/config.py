import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "data" / "app_config.json"

DEFAULT_CONFIG = {
    "send_to_snow_email": "",
    "email_subject_prefix": "",
    "default_parser_tab": "errors",
    "collapse_warnings_by_default": True
}

def load_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
