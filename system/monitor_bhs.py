import json
import os
import sys
import time
import subprocess

# Add the scripts directory to path
sys.path.append('/home/team/shared/scripts')
from calculate_bhs import calculate_bhs

SHARED_DIR = '/home/team/shared'
BHS_DATA_PATH = os.path.join(SHARED_DIR, 'brand_health_score.json')
DASHBOARD_DATA_PATH = os.path.join(SHARED_DIR, 'dashboard_data.json')
CVDB_PATH = os.path.join(SHARED_DIR, 'client_vector_db.json')

def get_latest_bhs():
    if not os.path.exists(BHS_DATA_PATH):
        return None
    with open(BHS_DATA_PATH, 'r') as f:
        return json.load(f)

def check_brand_violations():
    if not os.path.exists(CVDB_PATH):
        return False, ""
    try:
        with open(CVDB_PATH, 'r') as f:
            db = json.load(f)
        logs = db.get('validation_log', [])
        # Check for REJECTED status in the last 5 logs
        for entry in logs[-5:]:
            if entry.get('action') == 'REJECTED':
                return True, f"Brand Violation: {entry.get('notes')}"
    except:
        pass
    return False, ""

def trigger_red_line_alert(score, reason):
    print(f"!!! RED-LINE ALERT TRIGGERED: {reason} (Score: {score}) !!!")
    
    # 1. Update Dashboard
    if os.path.exists(DASHBOARD_DATA_PATH):
        try:
            with open(DASHBOARD_DATA_PATH, 'r') as f:
                data = json.load(f)
            
            data['global_status'] = "RED-LINE EMERGENCY"
            data['red_line_status'] = "ACTIVE"
            data['daily_digest'] = f"!!! AUTOMATED RED-LINE TRIGGER !!!\nReason: {reason}\nBHS Score: {score}\nCrisis commander notified."
            
            with open(DASHBOARD_DATA_PATH, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Dashboard update error: {e}")

    # 2. Automated Messaging via Task (Equivalent to waking up agent-mgr)
    alert_msg = f"CRITICAL: RED-LINE ALERT. BHS={score}. Reason: {reason}. Triggered by Automated Monitor."
    task_id = f"alert-{int(time.time())}"
    sql = f"INSERT INTO tasks (id, title, description, status, assigned_to, created_by) VALUES ('{task_id}', 'RED-LINE ALERT: {reason}', '{alert_msg}', 'backlog', 'agent-mgr', 'agent-ci-agent')"
    
    try:
        subprocess.run(["team-db", sql], check=True)
        print(f"Sent RED-LINE ALERT to Marketing Manager (Task ID: {task_id})")
    except:
        print("Failed to send automated alert via team-db.")

METRICS_PATH = os.path.join(SHARED_DIR, 'performance_metrics.json')

def get_latest_metrics(client_id="novatech-solutions"):
    if not os.path.exists(METRICS_PATH):
        return None
    try:
        with open(METRICS_PATH, 'r') as f:
            metrics_all = json.load(f)
        return metrics_all.get(client_id)
    except:
        return None

def monitor_cycle():
    # 1. Calculate Score
    bhs_raw = get_latest_bhs()
    metrics = get_latest_metrics()
    
    if not bhs_raw or not metrics:
        print("Waiting for data files...")
        return
    
    pillars = bhs_raw.get('pillars', {})
    
    # Use metrics for ROAS/CAC
    res = calculate_bhs(
        roas_actual=metrics['roas']['actual'],
        roas_target=metrics['roas']['target'],
        cac_actual=metrics['cac']['actual'],
        cac_target=metrics['cac']['target'],
        alignment=pillars.get('alignment', {}).get('score', 90),
        velocity=pillars.get('velocity', {}).get('score', 80),
        sentiment=pillars.get('sentiment', {}).get('score', 85)
    )
    
    score = res['overall_score']
    print(f"Current BHS Score: {score}")

    # 2. Check Thresholds
    violation, v_reason = check_brand_violations()
    
    if score < 50:
        trigger_red_line_alert(score, "BHS Score below critical threshold")
    elif violation:
        trigger_red_line_alert(score, v_reason)
    else:
        print("Agency status: NORMAL")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        print("Starting BHS Crisis Monitor...")
        while True:
            monitor_cycle()
            time.sleep(60)
    else:
        monitor_cycle()
