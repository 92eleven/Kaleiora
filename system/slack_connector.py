#!/usr/bin/env python3
"""Slack connector - sends messages via webhook. Mock mode when no URL."""
import json, os
from scripts.config_loader import Config

def send_slack_message(message):
    cfg = Config().get("slack")
    webhook = cfg.get("webhook_url", "")
    if not webhook:
        print(f"[MOCK - NOT LIVE] Slack message would be sent: {message[:100]}...")
        return {"status": "mock", "note": "MOCK - Configure SLACK_WEBHOOK_URL to send live"}
    try:
        import requests
        r = requests.post(webhook, json={"text": message}, timeout=5)
        if r.status_code == 200:
            return {"status": "sent"}
        return {"status": "error", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "error": str(e)}
