import json
import os
import time
import sys
from datetime import datetime

# Add the scripts directory to path so we can import calculate_bhs
sys.path.append('/home/team/shared/scripts')
try:
    from calculate_bhs import calculate_bhs
except ImportError:
    # Fallback if path is different
    sys.path.append('/home/team/shared')
    from scripts.calculate_bhs import calculate_bhs

BHS_DATA_PATH = '/home/team/shared/brand_health_score.json'
METRICS_PATH = '/home/team/shared/performance_metrics.json'
DASHBOARD_DATA_PATH = '/home/team/shared/dashboard_data.json'

def sync_bhs(client_id="novatech-solutions"):
    try:
        # 1. Read the Brand Health Score raw data (for Alignment, Velocity, Sentiment)
        # These are usually updated by the CI Agent or Brand Custodian
        if not os.path.exists(BHS_DATA_PATH):
            print(f"Warning: {BHS_DATA_PATH} not found. Using defaults.")
            alignment, velocity, sentiment = 90, 80, 85
        else:
            with open(BHS_DATA_PATH, 'r') as f:
                bhs_raw = json.load(f)
            pillars = bhs_raw.get('pillars', {})
            # We use 'score' or 'actual' depending on what's available
            # If actual is < 10, it's likely a ratio (like 0.8 for 80%)
            def normalize_score(pillar_data, default):
                val = pillar_data.get('actual', pillar_data.get('score', default))
                if val < 2.0: # Likely a ratio
                    return val * 100
                return val

            alignment = normalize_score(pillars.get('alignment', {}), 90)
            velocity = normalize_score(pillars.get('velocity', {}), 80)
            sentiment = normalize_score(pillars.get('sentiment', {}), 85)

        # 2. Calculate new BHS using calculate_bhs which now reads performance_metrics.json directly
        result = calculate_bhs(
            client_id=client_id,
            alignment=alignment,
            velocity=velocity,
            sentiment=sentiment
        )

        # 3. Update brand_health_score.json (Intermediate Store)
        # This ensures other scripts like monitor_bhs.py see the same fresh data
        bhs_update = {
            "client_name": client_id,
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "overall_score": result['overall_score'],
            "status": result['status'],
            "color": result['color'],
            "pillars": result['pillars'],
            "trend": "Synchronized"
        }
        with open(BHS_DATA_PATH, 'w') as f:
            json.dump(bhs_update, f, indent=2)

        # 4. Update Dashboard Data
        if not os.path.exists(DASHBOARD_DATA_PATH):
            print(f"Error: {DASHBOARD_DATA_PATH} not found.")
            return

        with open(DASHBOARD_DATA_PATH, 'r') as f:
            dashboard_data = json.load(f)

        dashboard_data['health_score'] = result['overall_score']
        dashboard_data['global_status'] = result['status']
        
        # Sync Red-Line status
        if result['status'] == "RED-LINE":
            dashboard_data['red_line_status'] = "ACTIVE"
        else:
            dashboard_data['red_line_status'] = "OPTIMIZED"
            # If we were in emergency, clear the digest if it was a BHS or Score trigger
            current_digest = dashboard_data.get('daily_digest', '')
            if "BHS Score" in current_digest or "Brand Health Score" in current_digest or "RED-LINE TRIGGER" in current_digest:
                dashboard_data['daily_digest'] = f"Status restored to {result['status']}. Brand Health Score: {result['overall_score']} (Sync: {client_id})"
        
        # Update metrics on dashboard
        metrics = result['pillars']
        dashboard_data['metrics']['roas'] = f"{metrics['roas']['actual']}x"
        dashboard_data['metrics']['cac'] = f"${metrics['cac']['actual']:.2f}"
        
        # Update project status if matching client_id
        for project in dashboard_data.get('projects', []):
            if project['name'] == client_id or (client_id == "novatech-solutions" and project['name'] == "NovaTech Solutions"):
                project['updated'] = "Just now"

        dashboard_data['updated_at'] = datetime.utcnow().isoformat() + "Z"

        with open(DASHBOARD_DATA_PATH, 'w') as f:
            json.dump(dashboard_data, f, indent=2)

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sync Complete: Client={client_id}, BHS={result['overall_score']}, Status={result['status']}")

    except Exception as e:
        print(f"Error syncing BHS: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        print("Starting Enhanced BHS Sync Loop (every 60s)...")
        while True:
            sync_bhs()
            time.sleep(60)
    else:
        sync_bhs()
