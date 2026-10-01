#!/usr/bin/env python3
"""
Kaleiora Quality Gate Validator
Validates creative assets against a client's brand profile in the Vector DB.
Usage: python3 validate_asset.py <client_id> <asset_file> <db_path>
"""
import json
import sys
import os

if len(sys.argv) != 4:
    print("Usage: validate_asset.py <client_id> <asset_file> <db_path>", file=sys.stderr)
    sys.exit(1)

client_id = sys.argv[1]
asset_file = sys.argv[2]
db_path = sys.argv[3]

# Read DB
with open(db_path) as f:
    db = json.load(f)

c = db.get('clients', {}).get(client_id)
if not c:
    print(f'ERROR: Client "{client_id}" not found.', file=sys.stderr)
    sys.exit(1)

# Read asset
with open(asset_file) as f:
    asset = json.load(f)

brand = c.get('brand_guidelines', {})
tone = c.get('tone_of_voice', {})

# Validation engine
issues = []
warnings = []
passes = []

do_say = tone.get('do_say', [])
dont_say = tone.get('dont_say', [])
asset_content = json.dumps(asset).lower()

for d in dont_say:
    if d.lower() in asset_content:
        issues.append(f'TONE VIOLATION: Content contains "{d}" which is in the dont_say list')

for d in do_say:
    if d.lower() not in asset_content:
        warnings.append(f'TONE SUGGESTION: Content could include "{d}" from do_say recommendations')

preferred = tone.get('vocabulary', {}).get('preferred_terms', [])
avoid = tone.get('vocabulary', {}).get('avoid_terms', [])
for a in avoid:
    if a.lower() in asset_content:
        issues.append(f'VOCABULARY VIOLATION: Avoid term "{a}" found in content')

for p in preferred:
    if p.lower() not in asset_content and asset.get('type') in ['copy', 'social', 'email']:
        warnings.append(f'VOCABULARY SUGGESTION: Preferred term "{p}" not found in content')

for msg in brand.get('key_messages', []):
    if msg.lower() in asset_content:
        passes.append(f'KEY MESSAGE: "{msg}" is reflected in the asset')

# Determine result
import uuid
asset_id = str(uuid.uuid4())

if len(issues) > 0:
    result = 'REJECTED'
    notes = 'FAILED QUALITY GATE: ' + '; '.join(issues)
elif len(warnings) > 0:
    result = 'PASSED_WITH_WARNINGS'
    notes = 'PASSED QUALITY GATE with recommendations: ' + '; '.join(warnings[:3])
else:
    result = 'APPROVED'
    notes = 'PASSED QUALITY GATE - All brand checks passed'

# Add validation log entry
log_entry = {
    'timestamp': os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip(),
    'asset_id': asset_id,
    'client_id': client_id,
    'asset_title': asset.get('title', 'unknown'),
    'asset_type': asset.get('type', 'unknown'),
    'action': result,
    'validator': 'agent-brand-custodian',
    'notes': notes,
    'details': {'issues': issues, 'warnings': warnings, 'passes': passes},
    'vector_db_references': [
        'brand_guidelines.key_messages',
        'tone_of_voice.do_say',
        'tone_of_voice.dont_say',
        'tone_of_voice.vocabulary'
    ]
}
db.setdefault('validation_log', []).append(log_entry)

# If passed, add to validated assets
if result in ['APPROVED', 'PASSED_WITH_WARNINGS']:
    asset['asset_id'] = asset_id
    asset['created_by'] = 'quality_gate'
    asset['validated_at'] = log_entry['timestamp']
    asset['approved'] = True
    asset['delivered_at'] = None
    asset['validation_notes'] = notes
    c.setdefault('validated_assets', []).append(asset)
    c['updated_at'] = log_entry['timestamp']

db['clients'][client_id] = c
db['last_updated'] = log_entry['timestamp']

# Write updated DB
with open(db_path, 'w') as f:
    json.dump(db, f, indent=2)

# Print results to stderr
print(f'\n=== QUALITY GATE RESULT ===', file=sys.stderr)
print(f'Asset: {asset.get("title","?")} ({asset.get("type","?")})', file=sys.stderr)
print(f'Result: {result}', file=sys.stderr)
print(f'Asset ID: {asset_id}', file=sys.stderr)
print(f'Notes: {notes}', file=sys.stderr)
if passes:
    print(f'Passes: {len(passes)} checks passed', file=sys.stderr)
if warnings:
    print(f'Warnings: {len(warnings)}', file=sys.stderr)
if issues:
    print(f'Issues: {len(issues)} - REJECTED', file=sys.stderr)
print('============================\n', file=sys.stderr)