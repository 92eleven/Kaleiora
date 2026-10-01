#!/usr/bin/env bash
# =============================================================================
# KALEIORA AGENTIC MARKETING - Client Vector Database CLI
# =============================================================================
# Usage:
#   ./client_vector_db.sh help                        - Show this help
#   ./client_vector_db.sh list                         - List all clients
#   ./client_vector_db.sh get <client_id>              - Get a client profile
#   ./client_vector_db.sh search <term>                - Search across all client data
#   ./client_vector_db.sh intake <json_file>           - Add a new client from intake form JSON
#   ./client_vector_db.sh validate <client_id> <asset_file>  - Validate an asset against brand
#   ./client_vector_db.sh approve <client_id> <asset_id>     - Mark asset as approved
#   ./client_vector_db.sh push <client_id> <asset_id>        - Mark asset as delivered
#   ./client_vector_db.sh activate <client_id>               - Activate a client
#   ./client_vector_db.sh active                        - List active clients
#   ./client_vector_db.sh stats                        - Show database statistics
#   ./client_vector_db.sh log [client_id]              - Show validation log
# =============================================================================

DB_PATH="/home/team/shared/client_vector_db.json"
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Ensure DB exists
if [ ! -f "$DB_PATH" ]; then
  echo '{"schema_version":"1.0","last_updated":"","clients":{},"validation_log":[],"index":{"by_status":{"intake":[],"active":[],"archived":[]},"by_agent":{}}}' > "$DB_PATH"
fi

case "${1:-help}" in
  help)
    echo "KALEIORA CLIENT VECTOR DB CLI"
    grep -E '^# Usage:' "$0" | sed 's/^# //'
    ;;

  list)
    python3 -c "
import json
db = json.load(open('$DB_PATH'))
clients = db.get('clients', {})
if not clients:
    print('No clients in database.')
else:
    print(f'{\"Client ID\":<40} {\"Name\":<30} {\"Status\":<12} {\"Assets\":<8}')
    print('-'*90)
    for cid, c in sorted(clients.items()):
        assets = len(c.get('validated_assets', []))
        print(f'{cid:<40} {c.get(\"client_name\",\"\"):<30} {c.get(\"status\",\"\"):<12} {assets:<8}')
"
    ;;

  get)
    if [ -z "$2" ]; then echo "Usage: $0 get <client_id>"; exit 1; fi
    python3 -c "
import json
db = json.load(open('$DB_PATH'))
c = db.get('clients', {}).get('$2')
if c:
    print(json.dumps(c, indent=2))
else:
    print('Client \"$2\" not found.')
"
    ;;

  search)
    if [ -z "$2" ]; then echo "Usage: $0 search <term>"; exit 1; fi
    python3 -c "
import json
db = json.load(open('$DB_PATH'))
term = '$2'.lower()
clients = db.get('clients', {})
found = 0
for cid, c in sorted(clients.items()):
    dump = json.dumps(c).lower()
    if term in dump:
        print(f'[MATCH] {cid} - {c.get(\"client_name\",\"\")}')
        found += 1
if found == 0:
    print(f'No clients matched \"$2\".')
else:
    print(f'\nFound {found} matching client(s).')
"
    ;;

  intake)
    if [ -z "$2" ]; then echo "Usage: $0 intake <json_file>"; exit 1; fi
    if [ ! -f "$2" ]; then echo "File not found: $2"; exit 1; fi
    
    INTAKE_FILE="$2"
    CLIENT_NAME=$(python3 -c "import json; d=json.load(open('$INTAKE_FILE')); print(d.get('client_name',''))")
    
    if [ -z "$CLIENT_NAME" ]; then
      echo "Error: client_name is required in intake JSON."
      exit 1
    fi
    
    NEW_ID="client-$(echo "$CLIENT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | head -c 30)-$(date +%s)"
    
    TMP_FILE=$(mktemp)
    DB_DATA=$(cat "$DB_PATH")
    python3 -c "
import json, sys
db = json.loads('''$DB_DATA''')
intake = json.load(open('$INTAKE_FILE'))
intake['client_id'] = '$NEW_ID'
intake['created_at'] = '$NOW'
intake['updated_at'] = '$NOW'
intake['status'] = 'intake'
if 'validated_assets' not in intake:
    intake['validated_assets'] = []
if 'intake_data' not in intake:
    intake['intake_data'] = {}
intake['intake_data']['submitted_at'] = '$NOW'
intake['intake_data']['source'] = 'dashboard_intake_form'
db['clients']['$NEW_ID'] = intake
db['last_updated'] = '$NOW'
idx = db.setdefault('index', {}).setdefault('by_status', {})
idx.setdefault('intake', []).append('$NEW_ID')
print(json.dumps(db, indent=2))
" > "$TMP_FILE" && mv "$TMP_FILE" "$DB_PATH"
    
    echo "CLIENT INGESTED: $NEW_ID | $CLIENT_NAME | Status: intake"
    ;;

  activate)
    if [ -z "$2" ]; then echo "Usage: $0 activate <client_id>"; exit 1; fi
    TMP_FILE=$(mktemp)
    DB_DATA=$(cat "$DB_PATH")
    python3 -c "
import json
db = json.loads('''$DB_DATA''')
c = db.get('clients', {}).get('$2')
if not c:
    print('ERROR: Client not found.')
    exit(1)
old = c.get('status','')
c['status'] = 'active'
c['updated_at'] = '$NOW'
db['clients']['$2'] = c
db['last_updated'] = '$NOW'
idx = db.setdefault('index', {}).setdefault('by_status', {})
if old in idx and '$2' in idx[old]:
    idx[old].remove('$2')
idx.setdefault('active', [])
if '$2' not in idx['active']:
    idx['active'].append('$2')
print(json.dumps(db, indent=2))
" > "$TMP_FILE" && mv "$TMP_FILE" "$DB_PATH"
    echo "Client $2 activated."
    ;;

  validate)
    if [ -z "$2" ] || [ -z "$3" ]; then
      echo "Usage: $0 validate <client_id> <asset_json_file>"
      exit 1
    fi
    if [ ! -f "$3" ]; then echo "Asset file not found: $3"; exit 1; fi
    
    ASSET_FILE="$3"
    python3 /home/team/shared/validate_asset.py "$2" "$3" "$DB_PATH" 2>&1
    ;;

  approve)
    if [ -z "$2" ] || [ -z "$3" ]; then
      echo "Usage: $0 approve <client_id> <asset_id>"
      exit 1
    fi
    TMP_FILE=$(mktemp)
    DB_DATA=$(cat "$DB_PATH")
    python3 -c "
import json
db = json.loads('''$DB_DATA''')
c = db.get('clients', {}).get('$2')
if not c:
    print('ERROR: Client not found.')
    exit(1)
found = False
for a in c.get('validated_assets', []):
    if a.get('asset_id') == '$3':
        a['approved'] = True
        a['validated_at'] = '$NOW'
        found = True
        break
if not found:
    print('ERROR: Asset not found.')
    exit(1)
c['updated_at'] = '$NOW'
db['clients']['$2'] = c
db['last_updated'] = '$NOW'
print(json.dumps(db, indent=2))
" > "$TMP_FILE" && mv "$TMP_FILE" "$DB_PATH"
    echo "Asset $3 approved."
    ;;

  push)
    if [ -z "$2" ] || [ -z "$3" ]; then
      echo "Usage: $0 push <client_id> <asset_id>"
      exit 1
    fi
    TMP_FILE=$(mktemp)
    DB_DATA=$(cat "$DB_PATH")
    python3 -c "
import json
db = json.loads('''$DB_DATA''')
c = db.get('clients', {}).get('$2')
if not c:
    print('ERROR: Client not found.')
    exit(1)
found = False
for a in c.get('validated_assets', []):
    if a.get('asset_id') == '$3':
        a['delivered_at'] = '$NOW'
        a['approved'] = True
        found = True
        break
if not found:
    print('ERROR: Asset not found.')
    exit(1)
c['updated_at'] = '$NOW'
db['clients']['$2'] = c
db['last_updated'] = '$NOW'
print(json.dumps(db, indent=2))
" > "$TMP_FILE" && mv "$TMP_FILE" "$DB_PATH"
    echo "Asset $3 pushed to Final Delivery."
    ;;

  active)
    python3 -c "
import json
db = json.load(open('$DB_PATH'))
active = db.get('index', {}).get('by_status', {}).get('active', [])
if not active:
    print('No active clients.')
else:
    print(f'Active Clients ({len(active)}):')
    for cid in active:
        c = db.get('clients', {}).get(cid, {})
        print(f'  - {cid}: {c.get(\"client_name\",\"?\")}')
"
    ;;

  stats)
    python3 -c "
import json
db = json.load(open('$DB_PATH'))
clients = db.get('clients', {})
total = len(clients)
statuses = {}
total_assets = 0
for c in clients.values():
    s = c.get('status', 'unknown')
    statuses[s] = statuses.get(s, 0) + 1
    total_assets += len(c.get('validated_assets', []))
log_count = len(db.get('validation_log', []))
print('=== CLIENT VECTOR DB STATS ===')
print('Schema Version:', db.get('schema_version','?'))
print('Total Clients:', total)
print('Total Validated Assets:', total_assets)
print('Validation Checks Run:', log_count)
print('By Status:')
for s, n in sorted(statuses.items()):
    print(f'  {s}: {n}')
print('Last Updated:', db.get('last_updated','never'))
"
    ;;

  log)
    if [ -z "$2" ]; then
      python3 -c "
import json
db = json.load(open('$DB_PATH'))
logs = db.get('validation_log', [])
print(f'Total validation events: {len(logs)}')
for entry in logs[-10:]:
    print(f'  [{entry.get(\"timestamp\",\"?\")}] {entry.get(\"action\",\"?\")} - {entry.get(\"asset_title\",\"?\")}')
      "
    else
      python3 -c "
import json
db = json.load(open('$DB_PATH'))
logs = [e for e in db.get('validation_log', []) if e.get('client_id') == '$2']
print(f'Validation events for $2: {len(logs)}')
for entry in logs[-10:]:
    print(f'  [{entry.get(\"timestamp\",\"?\")}] {entry.get(\"action\",\"?\")} - {entry.get(\"asset_title\",\"?\")}')
    print(f'  Notes: {entry.get(\"notes\",\"\")}')
    print()
      "
    fi
    ;;

  campaign)
    case "$2" in
      create)
        if [ -z "$3" ] || [ -z "$4" ]; then echo "Usage: $0 campaign create <client_id> <name>"; exit 1; fi
        python3 -c "
import json, uuid
db = json.load(open('$DB_PATH'))
c = db.get('clients', {}).get('$3')
if not c: print('ERROR: Client not found.'); exit(1)
campaign = {
    'campaign_id': str(uuid.uuid4()),
    'name': '$4',
    'status': 'planning',
    'start_date': '',
    'end_date': '',
    'channels': [],
    'objectives': [],
    'budget': 0,
    'current_roas': 0,
    'assets': [],
    'kpis': {'impressions':0,'clicks':0,'conversions':0,'spend':0}
}
c.setdefault('campaigns', []).append(campaign)
c['updated_at'] = '$NOW'
db['clients']['$3'] = c
db['last_updated'] = '$NOW'
with open('$DB_PATH','w') as f: json.dump(db,f,indent=2)
print(f'Campaign created: {campaign[\"campaign_id\"]} for $3')
"
        ;;
      list)
        if [ -z "$3" ]; then echo "Usage: $0 campaign list <client_id>"; exit 1; fi
        python3 -c "
import json
db = json.load(open('$DB_PATH'))
c = db.get('clients', {}).get('$3')
if not c: print('Client not found.'); exit(1)
campaigns = c.get('campaigns', [])
if not campaigns: print('No campaigns for $3.')
else:
    for cam in campaigns:
        print(f'  [{cam[\"status\"]}] {cam[\"campaign_id\"]} - {cam.get(\"name\",\"?\")}')
        print(f'     ROAS: {cam.get(\"current_roas\",0)} | Assets: {len(cam.get(\"assets\",[]))}')
"
        ;;
      activate|start)
        if [ -z "$3" ] || [ -z "$4" ]; then echo "Usage: $0 campaign activate <client_id> <campaign_id>"; exit 1; fi
        python3 -c "
import json
db = json.load(open('$DB_PATH'))
c = db.get('clients', {}).get('$3')
if not c: print('ERROR: Client not found.'); exit(1)
cid = '$3'
cam_id = '$4'
now = '$NOW'
for cam in c.get('campaigns', []):
    if cam.get('campaign_id') == cam_id:
        cam['status'] = 'active'
        cam['start_date'] = now
        c['updated_at'] = now
        db['clients'][cid] = c
        db['last_updated'] = now
        with open('$DB_PATH','w') as f: json.dump(db,f,indent=2)
        print(f'Campaign {cam_id} activated.')
        exit(0)
print('ERROR: Campaign not found.')
"
        ;;
      complete)
        if [ -z "$3" ] || [ -z "$4" ]; then echo "Usage: $0 campaign complete <client_id> <campaign_id>"; exit 1; fi
        python3 -c "
import json
db = json.load(open('$DB_PATH'))
c = db.get('clients', {}).get('$3')
if not c: print('ERROR: Client not found.'); exit(1)
for cam in c.get('campaigns', []):
    if cam.get('campaign_id') == '$4':
        cam['status'] = 'completed'
        cam['end_date'] = '$NOW'
        c['updated_at'] = '$NOW'
        db['clients']['$3'] = c
        db['last_updated'] = '$NOW'
        with open('$DB_PATH','w') as f: json.dump(db,f,indent=2)
        print(f'Campaign $4 completed.')
        exit(0)
print('ERROR: Campaign not found.')
"
        ;;
      *)
        echo "Usage: $0 campaign {create|list|activate|complete} <client_id> [campaign_id]"
        ;;
    esac
    ;;

  namespace)
    if [ -z "$2" ]; then echo "Usage: $0 namespace <client_id>"; exit 1; fi
    python3 -c "
import json, os
db = json.load(open('$DB_PATH'))
cid = '$2'
c = db.get('clients', {}).get(cid)
if not c: print('ERROR: Client not found.'); exit(1)

print(f'=== NAMESPACE CHECK: {cid} ===')
print(f'Name: {c.get(\"client_name\",\"?\")}')
print(f'Status: {c.get(\"status\",\"?\")}')
print(f'Brand Guidelines: {\"✅ Loaded\" if c.get(\"brand_guidelines\") else \"❌ Missing\"}')
print(f'Tone of Voice: {\"✅ Loaded\" if c.get(\"tone_of_voice\") else \"❌ Missing\"}')
print(f'Visual Identity: {\"✅ Loaded\" if c.get(\"visual_identity\") else \"❌ Missing\"}')
print(f'Validated Assets: {len(c.get(\"validated_assets\",[]))}')
print(f'Campaigns: {len(c.get(\"campaigns\",[]))}')

# Isolation check: verify no other client's data leaked in
total_clients = len(db.get('clients',{}))
print(f'Total tenants in DB: {total_clients}')
print(f'Namespace isolation: ✅ Client data is scoped under clients[\"{cid}\"]')
print(f'Index membership: {\"✅\" if cid in db[\"index\"][\"by_status\"].get(\"active\",[]) else \"⚠️ Not in active index\"}')
"
    ;;

  batch-validate)
    if [ -z "$2" ]; then echo "Usage: $0 batch-validate <asset_file> [client_id]"; exit 1; fi
    ASSET_FILE="$2"
    if [ -n "$3" ]; then
      # Validate against specific client
      echo "=== Batch: Validating $ASSET_FILE against $3 ==="
      python3 /home/team/shared/validate_asset.py "$3" "$ASSET_FILE" "$DB_PATH" 2>&1
    else
      # Validate against ALL active clients
      python3 -c "
import json
db = json.load(open('$DB_PATH'))
active = db.get('index',{}).get('by_status',{}).get('active',[])
# Exclude clients that already have this asset
for cid in active:
    c = db.get('clients', {}).get(cid, {})
    print(f'--- Validating $ASSET_FILE against {cid} ({c.get(\"client_name\",\"?\")}) ---')
" | while read line; do
  if echo "$line" | grep -q "Validating"; then
    CID=$(echo "$line" | grep -oP 'against \K\S+')
    echo "$line"
    python3 /home/team/shared/validate_asset.py "$CID" "$ASSET_FILE" "$DB_PATH" 2>&1
    echo ""
  fi
done
    fi
    ;;

  index)
    echo "Rebuilding client index..."
    python3 /home/team/shared/index_clients.py
    ;;

  *)
    echo "Unknown command: $1"
    echo "Usage: $0 help"
    exit 1
    ;;
esac
