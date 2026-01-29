# -----------------------------
# Ensure folders exist
# -----------------------------
New-Item -ItemType Directory -Force data | Out-Null
New-Item -ItemType Directory -Force utils | Out-Null
New-Item -ItemType Directory -Force templates | Out-Null

# -----------------------------
# app_config.json
# -----------------------------
@'
{
  "send_to_snow_email": "ServiceDesk@med.usc.edu",
  "email_subject_prefix": "[HL7 ERROR]",
  "default_parser_tab": "errors",
  "collapse_warnings_by_default": true
}
'@ | Set-Content data/app_config.json -Encoding UTF8

# -----------------------------
# utils/config.py
# -----------------------------
@'
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
'@ | Set-Content utils/config.py -Encoding UTF8

# -----------------------------
# templates/settings.html
# -----------------------------
@'
<!DOCTYPE html>
<html>
<head>
  <title>Settings - HL7 Tools</title>
  <link rel="icon" href="/static/favicon.ico">
  <style>
    body { font-family: Arial; background:#fafafa; padding:20px; }
    .section { background:#fff; padding:16px; border:1px solid #ccc; border-radius:6px; max-width:720px; margin-bottom:20px; }
    label { font-weight:bold; display:block; margin-top:10px; }
    input, select { width:100%; padding:8px; margin-top:4px; }
    button { margin-top:16px; background:#b71c1c; color:#fff; padding:10px; border:none; border-radius:4px; cursor:pointer; }
    button:hover { background:#8e0000; }
  </style>
</head>
<body>

<a href="/">← Back to Menu</a>
<h2>Settings</h2>

<form method="post">

  <div class="section">
    <h3>Send to SNOW</h3>
    <label>Default Service Desk Email</label>
    <input type="text" name="send_to_snow_email" value="{{ config.send_to_snow_email }}">
    <label>Email Subject Prefix</label>
    <input type="text" name="email_subject_prefix" value="{{ config.email_subject_prefix }}">
  </div>

  <div class="section">
    <h3>Parser Preferences</h3>
    <label>Default Tab</label>
    <select name="default_parser_tab">
      <option value="errors" {% if config.default_parser_tab=='errors' %}selected{% endif %}>Errors</option>
      <option value="raw" {% if config.default_parser_tab=='raw' %}selected{% endif %}>Raw HL7</option>
      <option value="pdf" {% if config.default_parser_tab=='pdf' %}selected{% endif %}>Original PDF</option>
    </select>

    <label>
      <input type="checkbox" name="collapse_warnings_by_default"
      {% if config.collapse_warnings_by_default %}checked{% endif %}>
      Collapse warnings by default
    </label>
  </div>

  <button type="submit">Save Settings</button>

</form>
</body>
</html>
'@ | Set-Content templates/settings.html -Encoding UTF8

# -----------------------------
# DONE
# -----------------------------
Write-Host "✔ Settings and tab infrastructure files created."
