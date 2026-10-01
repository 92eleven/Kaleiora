import requests
import json

def trigger_webhook(url, method='POST', data=None, headers=None):
    if not url:
        print("[SIMULATION] Webhook triggered (no URL provided)")
        return True
    
    try:
        if method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.get(url, params=data, headers=headers)
        
        response.raise_for_status()
        print(f"Webhook {method} to {url} successful.")
        return True
    except Exception as e:
        print(f"Webhook failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else None
    trigger_webhook(url, data={"event": "test"})
