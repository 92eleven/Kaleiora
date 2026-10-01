import os
import json
import requests

def send_slack_message(message, webhook_url=None):
    if not webhook_url:
        webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    
    if not webhook_url:
        print(f"[SIMULATION] Slack Message: {message}")
        return True
    
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Slack message sent successfully.")
        return True
    except Exception as e:
        print(f"Failed to send Slack message: {e}")
        return False

if __name__ == "__main__":
    import sys
    msg = sys.argv[1] if len(sys.argv) > 1 else "Test message from Kaleiora Agent"
    send_slack_message(msg)
