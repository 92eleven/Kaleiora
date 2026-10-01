#!/usr/bin/env python3
"""Kaleiora - Centralized Configuration Loader. Reads all API keys from config file."""
import json, os, sys

CONFIG_PATH = os.environ.get("KALEIORA_CONFIG", "/home/team/shared/config/api_keys.json")

class Config:
    def __init__(self, path=None):
        self.path = path or CONFIG_PATH
        self._data = self._load()

    def _load(self):
        try:
            with open(self.path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"integrations": {}}

    def get(self, integration_name):
        """Get integration config. Returns dict with all fields or empty dict."""
        return self._data.get("integrations", {}).get(integration_name, {})

    def is_enabled(self, integration_name):
        cfg = self.get(integration_name)
        # For cloudinary, check all 3 fields
        if integration_name == "cloudinary":
            return bool(cfg.get("cloud_name")) and bool(cfg.get("api_key")) and bool(cfg.get("api_secret"))
        # For makecom, check webhook_url
        if integration_name == "makecom":
            return bool(cfg.get("webhook_url"))
        # For others, check api_key
        return bool(cfg.get("api_key"))

    def status_report(self):
        """Return a dict of all integrations with their status."""
        integrations = self._data.get("integrations", {})
        report = {}
        for name in integrations:
            report[name] = {
                "configured": self.is_enabled(name),
                "status": "LIVE" if self.is_enabled(name) else "MOCK MODE",
                "label": "🟢 LIVE" if self.is_enabled(name) else "🟡 MOCK MODE"
            }
        return report

    def get_all_keys(self):
        return self._data.get("integrations", {})

if __name__ == "__main__":
    c = Config()
    print(json.dumps(c.status_report(), indent=2))
