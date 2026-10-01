import json
import os
import sys
import argparse
from datetime import datetime

METRICS_PATH = '/home/team/shared/performance_metrics.json'

def seed_data(client_id=None, client_name=None):
    # Load existing data if it exists
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, 'r') as f:
                data = json.load(f)
        except:
            data = {}
    else:
        data = {}

    if not client_id:
        # Default seed for NovaTech if no args
        client_id = "novatech-solutions"
        client_name = "NovaTech Solutions"
    
    data[client_id] = {
        "client_name": client_name,
        "roas": {
            "actual": 0.0,
            "target": 5.0
        },
        "cac": {
            "actual": 0.0,
            "target": 20.0
        },
        "conversions": 0,
        "impressions": 0,
        "spend": 0.0,
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }
    
    with open(METRICS_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Seeded performance metrics for {client_name} ({client_id}) to {METRICS_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Seed performance metrics for a client.')
    parser.add_argument('--client_id', type=str, help='The client ID')
    parser.add_argument('--client_name', type=str, help='The client name')
    
    args = parser.parse_args()
    seed_data(args.client_id, args.client_name)
