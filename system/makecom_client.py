#!/usr/bin/env python3
"""
Make.com Integration - Content scheduling and social posting via webhook.
Mock mode when MAKECOM_WEBHOOK_URL is empty.
"""
import json, os, uuid, datetime, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from config_loader import Config

DISTRIBUTION_LOG = "/home/team/shared/distribution_log.json"

class MakecomClient:
    def __init__(self):
        self.config = Config()
        self.cfg = self.config.get("makecom")
        self.webhook_url = self.cfg.get("webhook_url", "")
        self.enabled = bool(self.webhook_url)

    def is_live(self): return self.enabled

    def _log(self, entry):
        try:
            entries = []
            try:
                with open(DISTRIBUTION_LOG) as f: entries = json.load(f)
            except: pass
            entries.append(entry)
            with open(DISTRIBUTION_LOG, 'w') as f: json.dump(entries, f, indent=2)
        except: pass

    def schedule_post(self, client_name, asset_type, asset_path, caption, hashtags, platform, scheduled_time):
        """Send webhook to Make.com for scheduling. Mock mode when not configured."""
        send_id = f"makecom-{uuid.uuid4().hex[:12]}"
        timestamp = datetime.datetime.utcnow().isoformat()

        payload = {"client_name": client_name, "asset_type": asset_type, "asset_path": asset_path,
                   "caption": caption, "hashtags": hashtags, "platform": platform,
                   "scheduled_time": scheduled_time, "source": "Kaleiora Agentic Marketing"}

        if self.enabled:
            try:
                import requests
                resp = requests.post(self.webhook_url, json=payload, timeout=10)
                success = resp.status_code == 200
                entry = {"id": send_id, "timestamp": timestamp, "status": "sent" if success else "failed",
                         "payload_summary": {"client": client_name, "platform": platform, "asset": asset_type},
                         "response_code": resp.status_code}
                if not success:
                    # Retry once after 60 seconds
                    time.sleep(60)
                    resp2 = requests.post(self.webhook_url, json=payload, timeout=10)
                    if resp2.status_code == 200:
                        entry["status"] = "sent_after_retry"
                        entry["retry_success"] = True
                    else:
                        entry["retry_failed"] = True
                        from slack_connector import send_slack_message
                        send_slack_message(f"❌ Make.com webhook failed for {client_name} - {asset_type}")
                self._log(entry)
                return entry
            except Exception as e:
                entry = {"id": send_id, "timestamp": timestamp, "status": "error", "error": str(e)}
                self._log(entry)
                return entry
        else:
            entry = {"id": send_id, "timestamp": timestamp, "status": "MOCK - NOT LIVE",
                     "payload_summary": {"client": client_name, "platform": platform, "asset": asset_type},
                     "note": "MOCK - Configure MAKECOM_WEBHOOK_URL for live distribution",
                     "label": "READY FOR MANUAL DISTRIBUTION"}
            self._log(entry)
            return entry

if __name__ == "__main__":
    mc = MakecomClient()
    print("Make.com Status:", "LIVE" if mc.is_live() else "MOCK MODE")
    r = mc.schedule_post("NovaTech", "social_post", "/path/to/asset.png", "Check out our AI!", ["#AI", "#Tech"], "linkedin", "2026-06-10T10:00:00Z")
    print(json.dumps(r, indent=2))
