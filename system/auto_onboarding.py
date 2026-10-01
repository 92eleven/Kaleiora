import os
import json
import subprocess
import time
import re

SHARED_DIR = '/home/team/shared'
CVDB_SH = os.path.join(SHARED_DIR, 'client_vector_db.sh')
SEED_PY = os.path.join(SHARED_DIR, 'scripts/seed_performance_metrics.py')

def process_intake(file_path):
    print(f"Processing intake file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        client_name = data.get('client_name')
        if not client_name:
            print(f"Error: No client_name in {file_path}")
            return

        # Use absolute path for scripts and ensure shared dir is in path
        env = os.environ.copy()
        env['PYTHONPATH'] = SHARED_DIR + (':' + env.get('PYTHONPATH', '') if env.get('PYTHONPATH') else '')

        # 1. Run intake
        print(f"Running intake for {client_name}...")
        result = subprocess.run(['bash', CVDB_SH, 'intake', file_path], capture_output=True, text=True, env=env)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        # Extract NEW_ID from output: "CLIENT INGESTED: client-test-123 | Test | Status: intake"
        match = re.search(r'CLIENT INGESTED: (client-[\w-]+)', result.stdout)
        if not match:
            print("Error: Could not extract client_id from intake output")
            return
        
        client_id = match.group(1)
        print(f"Successfully ingested client with ID: {client_id}")

        # 2. Activate client
        print(f"Activating client {client_id}...")
        result = subprocess.run(['bash', CVDB_SH, 'activate', client_id], capture_output=True, text=True)
        print(result.stdout)

        # 3. Seed initial performance metrics
        print(f"Seeding metrics for {client_id}...")
        result = subprocess.run(['python3', SEED_PY, '--client_id', client_id, '--client_name', client_name], capture_output=True, text=True)
        print(result.stdout)

        # 4. Notify Brand Custodian (Simulated via a message or just a log for now as per instructions)
        # In a real scenario, I might use send_message to agent-brand-custodian
        # But the instructions say "The Brand Custodian should be auto-notified"
        # I'll use the 'team-db' to send an inbox message if I can, or just call send_message.
        # Actually, let's use the inbox table via team-db to be "agentic"
        notification_msg = f"New client onboarding complete: {client_name} ({client_id}). Please proceed with indexing and brand validation."
        subprocess.run(['team-db', f"INSERT INTO inbox (from_agent, to_agent, body) VALUES ('agent-dev', 'agent-brand-custodian', '{notification_msg}')"])
        
        print(f"Onboarding complete for {client_name}")

        # Move processed file to a 'processed' directory or just rename
        processed_dir = os.path.join(SHARED_DIR, 'processed_intakes')
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)
        
        new_path = os.path.join(processed_dir, os.path.basename(file_path))
        os.rename(file_path, new_path)
        print(f"Moved {file_path} to {new_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def watch_intakes():
    print(f"Watching for new intakes in {SHARED_DIR}...")
    while True:
        files = [f for f in os.listdir(SHARED_DIR) if f.startswith('intake_') and f.endswith('.json')]
        for f in files:
            file_path = os.path.join(SHARED_DIR, f)
            process_intake(file_path)
        time.sleep(10)

if __name__ == "__main__":
    watch_intakes()
