#!/usr/bin/env python3
"""
Kaleiora Agentic Marketing - Red-Line Crisis Protocol
======================================================
Real functional code, not documented concepts.

Auto-triggers when BHS < 50:
- Sets global status to RED-LINE-EMERGENCY
- Pauses all campaign generation
- Logs trigger with timestamp and score
- Sends Slack alert if configured
- Blocks all asset delivery until resolved
- Displays RED-LINE status on dashboard

Recovery:
- Accepts recovery asset
- Runs through Quality Gate
- If passes, resets to OPTIMIZED
- Logs resolution
- Resumes normal operations
"""
import json, os, datetime, sys, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.config_loader import Config

RED_LINE_LOG = "/home/team/shared/red_line_log.json"
DASHBOARD_FILE = "/home/team/shared/dashboard_data.json"
CAMPAIGN_LOCK_FILE = "/home/team/shared/.campaign_lock"
DB_PATH = "/home/team/shared/client_vector_db.json"

class RedLineProtocol:
    def __init__(self):
        self.config = Config()
        self.active = False
        self._load_state()

    def _load_state(self):
        try:
            with open(RED_LINE_LOG) as f:
                entries = json.load(f)
            # Check if there's an unresolved entry
            for entry in reversed(entries):
                if entry.get("resolution") is None:
                    self.active = True
                    return
        except: pass
        self.active = False

    def _log(self, entry):
        try:
            entries = []
            try:
                with open(RED_LINE_LOG) as f:
                    entries = json.load(f)
            except: pass
            entries.append(entry)
            with open(RED_LINE_LOG, 'w') as f:
                json.dump(entries, f, indent=2)
        except: pass

    def _update_dashboard(self, status, bhs_score, message=""):
        try:
            with open(DASHBOARD_FILE, 'r') as f:
                dash = json.load(f)
        except: dash = {}
        dash["global_status"] = status
        dash["red_line_status"] = "EMERGENCY" if status == "RED-LINE-EMERGENCY" else "CLEAR"
        dash["health_score"] = bhs_score
        if message:
            dash["daily_digest"] = f"🚨 {message}"
        dash["updated_at"] = datetime.datetime.utcnow().isoformat()
        try:
            with open(DASHBOARD_FILE, 'w') as f:
                json.dump(dash, f, indent=2)
        except: pass

    def _send_slack(self, message):
        cfg = self.config.get("slack")
        webhook = cfg.get("webhook_url", "")
        if webhook:
            try:
                import requests
                requests.post(webhook, json={"text": message}, timeout=5)
            except: pass

    def _set_campaign_lock(self, locked=True):
        try:
            if locked:
                with open(CAMPAIGN_LOCK_FILE, 'w') as f:
                    f.write(datetime.datetime.utcnow().isoformat())
            else:
                if os.path.exists(CAMPAIGN_LOCK_FILE):
                    os.remove(CAMPAIGN_LOCK_FILE)
        except: pass

    def is_campaign_generation_blocked(self):
        """Check if campaign generation is blocked by Red-Line."""
        return os.path.exists(CAMPAIGN_LOCK_FILE) or self.active

    def trigger(self, bhs_score, client_id="unknown", reason="BHS below threshold"):
        """
        Trigger Red-Line protocol. Called automatically when BHS < 50.
        Returns True if triggered successfully.
        """
        self.active = True
        timestamp = datetime.datetime.utcnow().isoformat()

        entry = {
            "timestamp": timestamp,
            "event": "RED-LINE-AUTO-TRIGGER",
            "score": bhs_score,
            "client_id": client_id,
            "reason": reason,
            "status": "ACTIVE",
            "resolution": None
        }
        self._log(entry)
        self._update_dashboard("RED-LINE-EMERGENCY", bhs_score, f"RED-LINE EMERGENCY: BHS={bhs_score} from {client_id}. Campaigns paused.")
        self._set_campaign_lock(True)
        self._send_slack(f"🚨 *RED-LINE EMERGENCY*\nBHS Score: {bhs_score}\nClient: {client_id}\nReason: {reason}\nAll campaigns paused. Recovery required.")

        print(f"🚨 RED-LINE TRIGGERED: BHS={bhs_score}, Client={client_id}")
        return True

    def recover(self, recovery_asset_path, recovery_notes=""):
        """
        Attempt recovery by running a recovery asset through Quality Gate.
        Returns dict with recovery result.
        """
        timestamp = datetime.datetime.utcnow().isoformat()
        resolution_id = f"resolved-{datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

        # Run through Quality Gate
        try:
            sys.path.insert(0, os.path.dirname(__file__))
            from quality_gate import run_quality_gate

            # Read the recovery asset
            if os.path.exists(recovery_asset_path):
                with open(recovery_asset_path, 'r') as f:
                    asset_data = json.load(f)
                asset_text = asset_data.get("content", "") or json.dumps(asset_data)
                client_id = asset_data.get("client_id", "unknown")
            else:
                asset_text = recovery_asset_path
                client_id = "unknown"

            qg_result = run_quality_gate(asset_text, client_id)
        except Exception as e:
            qg_result = {"overall_status": "FAIL", "error": str(e)}

        if qg_result.get("overall_status") == "PASS":
            # Recovery successful
            self.active = False
            self._set_campaign_lock(False)
            self._update_dashboard("OPTIMIZED", 85, f"✅ Red-Line resolved. Recovery asset: {os.path.basename(recovery_asset_path)}")

            # Log resolution
            entry = {
                "timestamp": timestamp,
                "event": "RED-LINE-RESOLUTION",
                "resolution_id": resolution_id,
                "recovery_asset": recovery_asset_path,
                "quality_gate_result": "PASS",
                "notes": recovery_notes,
                "status": "RESOLVED"
            }
            self._log(entry)
            self._send_slack(f"✅ *Red-Line Resolved*\nRecovery asset: {recovery_asset_path}\nQuality Gate: PASS\nStatus restored to OPTIMIZED.")

            return {"success": True, "resolution_id": resolution_id, "quality_gate_result": qg_result}
        else:
            # Recovery failed
            entry = {
                "timestamp": timestamp,
                "event": "RED-LINE-RECOVERY-FAILED",
                "resolution_id": resolution_id,
                "recovery_asset": recovery_asset_path,
                "quality_gate_result": "FAIL",
                "notes": recovery_notes,
                "status": "ACTIVE"
            }
            self._log(entry)
            self._send_slack(f"❌ *Red-Line Recovery Failed*\nAsset: {recovery_asset_path}\nQuality Gate: FAIL\nStatus remains RED-LINE-EMERGENCY.")

            return {"success": False, "resolution_id": resolution_id, "quality_gate_result": qg_result}

    def get_status(self):
        """Return current Red-Line status."""
        self._load_state()
        try:
            with open(RED_LINE_LOG) as f:
                entries = json.load(f)
            last = entries[-1] if entries else {}
        except: last = {}
        return {
            "active": self.active,
            "last_event": last,
            "campaigns_blocked": self.is_campaign_generation_blocked(),
            "history_count": len(entries) if 'entries' in dir() else 0
        }

if __name__ == "__main__":
    rl = RedLineProtocol()
    print("Red-Line Status:", json.dumps(rl.get_status(), indent=2))

    # Demo trigger
    print("\n--- Demo: Triggering Red-Line ---")
    rl.trigger(bhs_score=30, client_id="client-novatech-solutions-demo", reason="Automated test: BHS dropped to 30")

    print("\n--- Demo: Attempting Recovery ---")
    result = rl.recover("/home/team/shared/sample_asset_valid.json", "Test recovery after automated trigger")
    print(json.dumps(result, indent=2))

    print("\n--- Final Status ---")
    print(json.dumps(rl.get_status(), indent=2))
