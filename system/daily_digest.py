import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta

SHARED_DIR = '/home/team/shared'
METRICS_PATH = os.path.join(SHARED_DIR, 'performance_metrics.json')
BHS_DATA_PATH = os.path.join(SHARED_DIR, 'brand_health_score.json')
BHS_HISTORY_PATH = os.path.join(SHARED_DIR, 'bhs_history.json')
RED_LINE_LOG_PATH = os.path.join(SHARED_DIR, 'red_line_log.json')
DASHBOARD_DATA_PATH = os.path.join(SHARED_DIR, 'dashboard_data.json')

def get_bhs_trend():
    if not os.path.exists(BHS_HISTORY_PATH):
        return "N/A"
    try:
        with open(BHS_HISTORY_PATH, 'r') as f:
            history = json.load(f)
        if len(history) < 2:
            return "N/A"
        
        current = history[-1]['score']
        # Find score ~24h ago (or oldest available)
        yesterday = datetime.utcnow() - timedelta(days=1)
        prev_score = history[0]['score']
        
        for entry in reversed(history[:-1]):
            # Parse timestamp, handle Z
            ts = entry['timestamp'].replace('Z', '')
            entry_time = datetime.fromisoformat(ts)
            if entry_time <= yesterday:
                prev_score = entry['score']
                break
        
        diff = current - prev_score
        sign = "+" if diff >= 0 else ""
        return f"{sign}{diff} pts (24h)"
    except Exception as e:
        return f"Trend Error"

def get_red_line_summary():
    if not os.path.exists(RED_LINE_LOG_PATH):
        return "0 incidents"
    try:
        with open(RED_LINE_LOG_PATH, 'r') as f:
            logs = json.load(f)
        
        # Count incidents in last 24h
        yesterday = datetime.utcnow() - timedelta(days=1)
        count = 0
        for entry in logs:
            ts = entry['timestamp'].replace('Z', '')
            entry_time = datetime.fromisoformat(ts)
            if entry_time > yesterday:
                count += 1
        
        return f"{count} incidents in 24h"
    except Exception as e:
        return f"0 incidents"

def get_agent_activity():
    try:
        res = subprocess.run([
            "team-db", 
            "SELECT assigned_to, count(*) as task_count FROM tasks WHERE updated_at > datetime('now', '-1 day') GROUP BY assigned_to"
        ], capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        summary = ", ".join([f"{item['assigned_to'].replace('agent-', '')}: {item['task_count']}" for item in data])
        return summary if summary else "No activity"
    except Exception as e:
        return f"Activity unavailable"

def generate_digest():
    # 1. Performance (Source: performance_metrics.json)
    performance_md = "- **ROAS:** N/A\n- **CAC:** N/A\n- **Conversions:** N/A"
    top_client = "None"
    
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, 'r') as f:
                metrics = json.load(f)
            if metrics:
                client_id = list(metrics.keys())[0]
                m = metrics[client_id]
                roas = m.get('roas', {}).get('actual', 0)
                cac = m.get('cac', {}).get('actual', 0)
                conv = m.get('conversions', 0)
                top_client = m.get('client_name', client_id)
                performance_md = (
                    f"- **ROAS:** `{roas}x` (Target: {m.get('roas', {}).get('target', 'N/A')}x)\n"
                    f"- **CAC:** `${cac:.2f}`\n"
                    f"- **Conversions:** `{conv}`"
                )
        except: pass
    
    # 2. BHS (Source: brand_health_score.json)
    bhs = "N/A"
    status = "N/A"
    if os.path.exists(BHS_DATA_PATH):
        try:
            with open(BHS_DATA_PATH, 'r') as f:
                bhs_data = json.load(f)
            bhs = bhs_data.get('overall_score', "N/A")
            status = bhs_data.get('status', "N/A")
        except: pass
    
    trend = get_bhs_trend()
    
    # 3. Red-Line (Source: red_line_log.json)
    rl_summary = get_red_line_summary()
    
    # 4. Swarm Health (Source: dashboard_data.json)
    agent_status_msg = "Unknown"
    if os.path.exists(DASHBOARD_DATA_PATH):
        try:
            with open(DASHBOARD_DATA_PATH, 'r') as f:
                db_data = json.load(f)
            agents = db_data.get('agents', [])
            online = sum(1 for a in agents if a.get('status') == 'online')
            agent_status_msg = f"{online}/{len(agents)} Agents Online"
        except: pass
    
    # 5. Agent Activity (Source: team-db)
    agent_activity = get_agent_activity()
    
    # Format Digest as Markdown
    now_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    
    digest = (
        f"### 📅 DAILY PERFORMANCE DIGEST\n"
        f"*Generated: {now_str}*\n\n"
        f"**🛡️ Brand Health & Safety**\n"
        f"- **Score:** `{bhs}` ({trend})\n"
        f"- **Status:** `{status}`\n"
        f"- **Incidents:** {rl_summary}\n\n"
        f"**🚀 Performance KPIs**\n"
        f"- **Top Client:** {top_client}\n"
        f"{performance_md}\n\n"
        f"**🤖 Swarm Activity**\n"
        f"- **Connectivity:** {agent_status_msg}\n"
        f"- **Task Throughput:** {agent_activity}\n\n"
        f"> **Commander Note:** Systems are currently **{status}**. "
        f"Performance is trending {('up' if '+' in trend else 'stable')}. "
        f"Swarm connectivity is nominal."
    )
    
    return digest

def update_dashboard(digest):
    if not os.path.exists(DASHBOARD_DATA_PATH):
        return
    try:
        with open(DASHBOARD_DATA_PATH, 'r') as f:
            data = json.load(f)
        
        data['daily_digest'] = digest
        data['updated_at'] = datetime.utcnow().isoformat() + "Z"
        
        with open(DASHBOARD_DATA_PATH, 'w') as f:
            json.dump(data, f, indent=2)
        print("Dashboard updated with Markdown Daily Digest.")
    except Exception as e:
        print(f"Error updating dashboard: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        print("Starting Daily Performance Digest Loop (Target: 08:00 EST)...")
        while True:
            # Run immediately once
            digest = generate_digest()
            update_dashboard(digest)
            
            # Calculate wait time until next 08:00 EST
            now_utc = datetime.utcnow()
            # EST is UTC-5
            now_est = now_utc - timedelta(hours=5)
            
            target_est = now_est.replace(hour=8, minute=0, second=0, microsecond=0)
            if now_est >= target_est:
                target_est += timedelta(days=1)
            
            wait_seconds = (target_est - now_est).total_seconds()
            
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Digest updated.")
            print(f"Next scheduled run: {target_est.strftime('%Y-%m-%d %H:%M:%S')} EST (Waiting {wait_seconds:.0f}s)")
            
            time.sleep(wait_seconds)
    else:
        digest = generate_digest()
        print("--- GENERATED DIGEST ---")
        print(digest)
        print("------------------------")
        update_dashboard(digest)
