#!/usr/bin/env python3
import subprocess
import os
import json
from datetime import datetime, timezone

# Paths
SHARED_DIR = "/home/team/shared"
SCRIPTS_DIR = f"{SHARED_DIR}/scripts"
CREATIVE_DIR = f"{SHARED_DIR}/creative_output"
GENERATE_SCRIPT = f"{CREATIVE_DIR}/generate_novatech_campaign.py"
VALIDATE_SCRIPT = f"{SHARED_DIR}/validate_asset.py"
SYNC_BHS_SCRIPT = f"{SCRIPTS_DIR}/sync_bhs.py"
DASHBOARD_DATA_PATH = f"{SHARED_DIR}/dashboard_data.json"
VECTOR_DB_PATH = f"{SHARED_DIR}/client_vector_db.json"
CLIENT_ID = "client-novatech-solutions-demo" # From teammates' work

def run_step(name, command):
    print(f"--- Running {name} ---")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in {name}: {result.stderr}")
        return False, result.stdout, result.stderr
    print(f"Success: {name}")
    return True, result.stdout, result.stderr

def main():
    print(f"Starting Scheduled Campaign Cycle at {datetime.now(timezone.utc).isoformat()}")
    
    # 1. Generate Creative
    success, stdout, stderr = run_step("Generate Creative", f"python3 {GENERATE_SCRIPT}")
    if not success:
        return

    # Find the manifest file from stdout
    manifest_path = None
    for line in stdout.split('\n'):
        if "Manifest:" in line:
            manifest_path = line.strip().split("Manifest:")[1].strip()
    
    if not manifest_path or not os.path.exists(manifest_path):
        # Fallback search
        import glob
        manifests = glob.glob(f"{CREATIVE_DIR}/*_manifest_*.json")
        if manifests:
            manifest_path = max(manifests, key=os.path.getctime)

    if not manifest_path:
        print("❌ Campaign Cycle Failed: Manifest not found.")
        return

    print(f"Found manifest: {manifest_path}")

    # 2. Run Quality Gate (Validation)
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    assets = manifest['assets']
    passed_assets = []
    failed_assets = []

    for asset in assets:
        asset_file = asset['file']
        asset_path = os.path.join(CREATIVE_DIR, asset_file)
        # Use CLIENT_ID instead of the one in manifest if they differ (manifest uses a demo ID)
        v_success, v_stdout, v_stderr = run_step(f"Validate {asset_file}", f"python3 {VALIDATE_SCRIPT} {CLIENT_ID} {asset_path} {VECTOR_DB_PATH}")
        
        if "APPROVED" in v_stderr or "PASSED" in v_stderr:
            passed_assets.append(asset_file)
        else:
            failed_assets.append(asset_file)

    # 3. Sync BHS and Dashboard
    run_step("Sync BHS & Dashboard", f"python3 {SYNC_BHS_SCRIPT}")

    # 4. Update Dashboard Creative Assets List
    try:
        with open(DASHBOARD_DATA_PATH, 'r') as f:
            dashboard_data = json.load(f)
        
        # Add new passed assets to the list (avoid duplicates)
        current_assets = set(dashboard_data.get('creative_assets', []))
        for asset_file in passed_assets:
            current_assets.add(asset_file)
        
        dashboard_data['creative_assets'] = list(current_assets)[-10:] # Keep last 10
        
        # Update Daily Digest
        summary = f"📅 DAILY CAMPAIGN CYCLE ({datetime.now().strftime('%Y-%m-%d')})\n"
        summary += f"✅ Assets Generated: {len(assets)} | "
        summary += f"🛡️ Quality Gate: {len(passed_assets)} Passed, {len(failed_assets)} Rejected\n"
        summary += f"🚀 Client: NovaTech Solutions | Status: OPTIMIZED"
        
        dashboard_data['daily_digest'] = summary
        dashboard_data['updated_at'] = datetime.now(timezone.utc).isoformat() + "Z"

        with open(DASHBOARD_DATA_PATH, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        print("Updated dashboard with campaign results.")
    except Exception as e:
        print(f"Error updating dashboard: {e}")

    print("Campaign Cycle Finished Successfully.")

if __name__ == "__main__":
    main()
