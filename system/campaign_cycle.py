#!/usr/bin/env python3
import subprocess
import os
import json
import shutil
from datetime import datetime, timezone

# Paths
SHARED_DIR = "/home/team/shared"
SCRIPTS_DIR = f"{SHARED_DIR}/scripts"
CREATIVE_DIR = f"{SHARED_DIR}/creative_output"
ARCHIVE_DIR = f"{SHARED_DIR}/archive"
GENERATE_SCRIPT = f"{CREATIVE_DIR}/generate_novatech_campaign.py"
VALIDATE_CLI = f"{SHARED_DIR}/client_vector_db.sh"
SYNC_BHS_SCRIPT = f"{SCRIPTS_DIR}/sync_bhs.py"
DASHBOARD_DATA_PATH = f"{SHARED_DIR}/dashboard_data.json"
CLIENT_ID = "client-novatech-solutions-demo"

def run_step(name, command):
    print(f"--- Step: {name} ---")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in {name}: {result.stderr}")
        return False, result.stdout, result.stderr
    print(f"Success: {name}")
    return True, result.stdout, result.stderr

def main():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    print(f"Starting Campaign Cycle: {timestamp}")
    
    # Step 1: Trigger Creative Agent to generate assets
    success, stdout, stderr = run_step("1. Generate Creative Assets", f"python3 {GENERATE_SCRIPT}")
    if not success: return

    manifest_path = None
    for line in stdout.split('\n'):
        if "Manifest:" in line:
            manifest_path = line.strip().split("Manifest:")[1].strip()
    
    if not manifest_path or not os.path.exists(manifest_path):
        import glob
        manifests = glob.glob(f"{CREATIVE_DIR}/*_manifest_*.json")
        if manifests: manifest_path = max(manifests, key=os.path.getctime)

    if not manifest_path:
        print("❌ Error: Manifest not found.")
        return

    # Step 2: Run client_vector_db.sh validate on each asset
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    assets = manifest.get('assets', [])
    passed_assets = []
    
    for asset in assets:
        asset_file = asset['file']
        asset_path = os.path.join(CREATIVE_DIR, asset_file)
        v_success, v_stdout, v_stderr = run_step(f"2. Validate {asset_file}", f"{VALIDATE_CLI} validate {CLIENT_ID} {asset_path}")
        
        # client_vector_db.sh outputs pass/fail to stderr via validate_asset.py
        if "APPROVED" in v_stderr or "PASSED" in v_stderr:
            passed_assets.append(asset_path)

    # Step 3: Push passed assets to dashboard
    try:
        with open(DASHBOARD_DATA_PATH, 'r') as f:
            dashboard_data = json.load(f)
        
        current_assets = dashboard_data.get('creative_assets', [])
        for path in passed_assets:
            fname = os.path.basename(path)
            if fname not in current_assets:
                current_assets.append(fname)
        
        dashboard_data['creative_assets'] = current_assets[-12:] # Keep recent
        dashboard_data['updated_at'] = datetime.now(timezone.utc).isoformat() + "Z"
        
        with open(DASHBOARD_DATA_PATH, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        print("Step 3: Dashboard updated with passed assets.")
    except Exception as e:
        print(f"Error in Step 3: {e}")

    # Step 4: Calculate and log BHS
    run_step("4. Calculate and Log BHS", f"python3 {SYNC_BHS_SCRIPT}")

    # Step 5: Archive campaign results
    archive_path = os.path.join(ARCHIVE_DIR, f"campaign_{timestamp}")
    os.makedirs(archive_path, exist_ok=True)
    
    # Move manifest
    shutil.move(manifest_path, os.path.join(archive_path, os.path.basename(manifest_path)))
    
    # Move all assets listed in manifest
    for asset in assets:
        asset_file = asset['file']
        src = os.path.join(CREATIVE_DIR, asset_file)
        if os.path.exists(src):
            shutil.move(src, os.path.join(archive_path, asset_file))
            
    print(f"Step 5: Campaign archived to {archive_path}")
    print("Campaign Cycle Complete.")

if __name__ == "__main__":
    main()
