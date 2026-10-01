#!/usr/bin/env python3
"""
SendGrid Integration - Email campaign deployment.
Mock mode when SENDGRID_API_KEY is empty - saves as draft HTML.
"""
import json, os, uuid, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from config_loader import Config

EMAIL_LOG = "/home/team/shared/email_log.json"
EMAIL_DRAFTS_DIR = "/home/team/shared/email_drafts"

class SendGridClient:
    def __init__(self):
        self.config = Config()
        self.cfg = self.config.get("sendgrid")
        self.api_key = self.cfg.get("api_key", "")
        self.from_name = self.cfg.get("default_from_name", "Kaleiora Marketing")
        self.from_email = self.cfg.get("default_from_email", "marketing@kaleiora.ai")
        self.enabled = bool(self.api_key)
        os.makedirs(EMAIL_DRAFTS_DIR, exist_ok=True)

    def is_live(self): return self.enabled

    def _log(self, entry):
        try:
            entries = []
            try:
                with open(EMAIL_LOG) as f: entries = json.load(f)
            except: pass
            entries.append(entry)
            with open(EMAIL_LOG, 'w') as f: json.dump(entries, f, indent=2)
        except: pass

    def send_campaign(self, from_name, from_email, subject, preview_text, html_body, recipient_list, client_name="unknown"):
        """Send email campaign via SendGrid. Mock mode saves as draft HTML."""
        send_id = f"sendgrid-{uuid.uuid4().hex[:12]}"
        timestamp = datetime.datetime.utcnow().isoformat()

        if self.enabled:
            try:
                import sendgrid
                from sendgrid.helpers.mail import Mail, Email, To, Content
                sg = sendgrid.SendGridAPIClient(api_key=self.api_key)
                mail = Mail(Email(from_email, from_name), subject, Email(from_email), [To(r) for r in recipient_list],
                            Content("text/html", html_body))
                response = sg.send(mail)
                entry = {"id": send_id, "timestamp": timestamp, "status": "sent",
                         "subject": subject, "recipient_count": len(recipient_list),
                         "message_id": response.headers.get("X-Message-Id", "unknown"),
                         "client": client_name}
                self._log(entry)
                return entry
            except Exception as e:
                entry = {"id": send_id, "timestamp": timestamp, "status": "error", "error": str(e),
                         "subject": subject, "client": client_name}
                self._log(entry)
                from slack_connector import send_slack_message
                send_slack_message(f"❌ SendGrid send failed for '{subject}': {e}")
                return entry
        else:
            # Save as draft HTML
            draft_filename = f"email_draft_{client_name}_{subject[:30].replace(' ','_')}_{timestamp[:10]}.html"
            draft_path = os.path.join(EMAIL_DRAFTS_DIR, draft_filename)
            try:
                with open(draft_path, 'w') as f:
                    f.write(f"<!-- DRAFT - READY FOR MANUAL SEND -->\n")
                    f.write(f"<!-- From: {from_name} <{from_email}> -->\n")
                    f.write(f"<!-- Subject: {subject} -->\n")
                    f.write(f"<!-- Preview: {preview_text} -->\n")
                    f.write(f"<!-- Recipients: {len(recipient_list)} -->\n")
                    f.write(html_body)
            except: pass

            entry = {"id": send_id, "timestamp": timestamp, "status": "MOCK - NOT LIVE",
                     "subject": subject, "recipient_count": len(recipient_list),
                     "client": client_name, "draft_file": draft_path,
                     "label": "READY FOR MANUAL SEND",
                     "note": "MOCK - Configure SENDGRID_API_KEY for live email deployment"}
            self._log(entry)
            return entry

if __name__ == "__main__":
    sc = SendGridClient()
    print("SendGrid Status:", "LIVE" if sc.is_live() else "MOCK MODE")
    r = sc.send_campaign("Kaleiora", "marketing@kaleiora.ai", "Your AI Marketing Report", "Preview text",
                         "<h1>Hello!</h1><p>Your campaign is ready.</p>",
                         ["client@example.com"], "NovaTech")
    print(json.dumps(r, indent=2))
