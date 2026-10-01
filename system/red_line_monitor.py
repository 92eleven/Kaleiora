import json
import os
import sys
import time
import subprocess

# Path to the shared directory
SHARED_DIR = '/home/team/shared'
SCRIPTS_DIR = os.path.join(SHARED_DIR, 'scripts')
sys.path.append(SHARED_DIR) # Add this so 'integrations' can be found
sys.path.append(SCRIPTS_DIR)

from sync_bhs import sync_bhs
from integrations.connectors.slack_connector import send_slack_message
from integrations.connectors.campaign_connector import update_campaign_status

DASHBOARD_DATA_PATH = os.path.join(SHARED_DIR, 'dashboard_data.json')
RED_LINE_LOG_PATH = os.path.join(SHARED_DIR, 'red_line_log.json')

def log_red_line_event(score, reason):
    event = {
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "event": "RED-LINE_AUTO_TRIGGER",
        "score": score,
        "reason": reason,
        "status": "TRIGGERED"
    }
    
    events = []
    if os.path.exists(RED_LINE_LOG_PATH):
        try:
            with open(RED_LINE_LOG_PATH, 'r') as f:
                events = json.load(f)
        except:
            pass
            
    events.append(event)
    
    with open(RED_LINE_LOG_PATH, 'w') as f:
        json.dump(events, f, indent=2)

def alert_manager(score):
    alert_msg = f"CRITICAL ALERT: Brand Health Score has dropped to {score}. RED-LINE protocol has been automatically triggered. Please check the Command Center immediately."
    task_id = f"redline-{int(time.time())}"
    sql = f"INSERT INTO tasks (id, title, description, status, assigned_to, created_by) VALUES ('{task_id}', 'RED-LINE EMERGENCY ALERT', '{alert_msg}', 'backlog', 'agent-mgr', 'agent-ci-agent')"
    
    try:
        subprocess.run(["team-db", sql], check=True)
        print(f"Alert task created for agent-mgr: {task_id}")
    except Exception as e:
        print(f"Failed to create alert task: {e}")

def trigger_red_line(score):
    print(f"!!! CRITICAL: BHS score {score} is below 50. Triggering Red-Line Protocol. !!!")
    
    # 1. Update dashboard status
    if os.path.exists(DASHBOARD_DATA_PATH):
        try:
            with open(DASHBOARD_DATA_PATH, 'r') as f:
                data = json.load(f)
            
            data['global_status'] = "RED-LINE EMERGENCY"
            data['red_line_status'] = "ACTIVE"
            data['daily_digest'] = f"!!! RED-LINE EMERGENCY !!!\nAutomated monitor detected BHS drop to {score}.\nCrisis protocol initiated."
            
            with open(DASHBOARD_DATA_PATH, 'w') as f:
                json.dump(data, f, indent=2)
            print("Dashboard updated to RED-LINE EMERGENCY.")
        except Exception as e:
            print(f"Error updating dashboard: {e}")
    
    # 2. Log the event
    log_red_line_event(score, "BHS score fell below threshold (50)")
    
    # 3. Alert the Manager
    alert_manager(score)

    # 4. EXTERNAL INTEGRATIONS
    # Pause Campaigns
    update_campaign_status('PAUSED')
    
    # Send Slack Alert
    send_slack_message(f"🚨 RED-LINE EMERGENCY: Brand Health Score dropped to {score}. All campaigns have been PAUSED. Protocol Alpha initiated.")

def monitor_bhs():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running BHS Sync and Monitor...")
    # Run the sync
    sync_bhs()
    
    # Read the updated score
    if os.path.exists(DASHBOARD_DATA_PATH):
        try:
            with open(DASHBOARD_DATA_PATH, 'r') as f:
                data = json.load(f)
            
            score = data.get('health_score', 100)
            
            if score < 50 and data.get('red_line_status') != "ACTIVE":
                trigger_red_line(score)
                return True
            elif score >= 50 and data.get('red_line_status') == "ACTIVE":
                print("Note: System is in RED-LINE but score is recovering. Manual reset required.")
        except Exception as e:
            print(f"Error reading dashboard data: {e}")
            
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        print("Starting Red-Line Monitor Loop (every 60s)...")
        while True:
            monitor_bhs()
            time.sleep(60)
    else:
        monitor_bhs()
