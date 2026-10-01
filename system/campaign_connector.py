import json
import os

STATUS_FILE = '/home/team/shared/campaign_status.json'

def update_campaign_status(status):
    """
    Simulates pausing or resuming campaigns.
    status: 'PAUSED' or 'ACTIVE'
    """
    state = {
        "status": status,
        "last_updated": os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip()
    }
    
    with open(STATUS_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"Campaign status set to: {status}")
    
    # Also update dashboard data to reflect this if possible
    dashboard_path = '/home/team/shared/dashboard_data.json'
    if os.path.exists(dashboard_path):
        try:
            with open(dashboard_path, 'r') as f:
                data = json.load(f)
            
            data['campaign_status'] = status
            
            with open(dashboard_path, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass

if __name__ == "__main__":
    import sys
    action = sys.argv[1].upper() if len(sys.argv) > 1 else 'ACTIVE'
    update_campaign_status(action)
