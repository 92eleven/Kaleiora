import json
import sys
import os
from datetime import datetime

DASHBOARD_PATH = '/home/team/shared/dashboard_data.json'
METRICS_PATH = '/home/team/shared/performance_metrics.json'

def update_json_file(file_path, field, value, subfield=None, client_id=None):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return

    with open(file_path, 'r') as f:
        data = json.load(f)
    
    target = data
    if client_id and client_id in data:
        target = data[client_id]
    elif client_id:
        print(f"Error: Client {client_id} not found in {file_path}")
        return

    if subfield:
        if field not in target:
            target[field] = {}
        target[field][subfield] = value
    else:
        target[field] = value
        
    if 'last_updated' in target:
        target['last_updated'] = datetime.utcnow().isoformat() + "Z"
    elif 'updated_at' in target:
        target['updated_at'] = datetime.utcnow().isoformat() + "Z"

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {file_path}: {field}{'['+subfield+']' if subfield else ''} to {value}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 update_dashboard.py <field> <value> [subfield] [--client <client_id>]")
        sys.exit(1)
        
    field = sys.argv[1]
    value = sys.argv[2]
    
    subfield = None
    client_id = None
    
    args = sys.argv[3:]
    if args and not args[0].startswith('--'):
        subfield = args[0]
        args = args[1:]
    
    if '--client' in args:
        idx = args.index('--client')
        if idx + 1 < len(args):
            client_id = args[idx+1]

    # Try to convert value to numeric if possible
    try:
        if '.' in value:
            value = float(value)
        elif value.isdigit():
            value = int(value)
    except:
        pass
        
    # Determine which file to update
    metrics_fields = ['roas', 'cac', 'conversions', 'impressions', 'spend']
    
    if field in metrics_fields or client_id:
        update_json_file(METRICS_PATH, field, value, subfield, client_id or "novatech-solutions")
    else:
        update_json_file(DASHBOARD_PATH, field, value, subfield)
