from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import sys
import subprocess
import threading

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/submit_intake':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                # Save intake file
                client_name = data.get('client_name', 'unknown').replace(' ', '_')
                submission_file = f"/home/team/shared/intake_{client_name}.json"
                with open(submission_file, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"Intake received for {client_name}, saved to {submission_file}")
                
                # Auto-generate lead preview in background
                def generate_preview():
                    try:
                        script = "/home/team/shared/scripts/generate_lead_preview.py"
                        result = subprocess.run(
                            ["python3", script, submission_file],
                            capture_output=True, text=True, timeout=30
                        )
                        print(f"Lead preview generated for {client_name}: {result.stdout[:200]}")
                    except Exception as e:
                        print(f"Preview generation error: {e}")
                
                threading.Thread(target=generate_preview, daemon=True).start()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success", 
                    "message": "Sneak peek being generated!",
                    "preview": f"/lead_previews/"
                }).encode())
            except Exception as e:
                print(f"Error handling intake: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    os.chdir('/home/team/shared/')
    port = 8000
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f"Kaleiora Dashboard Server running on port {port}...")
    print(f"Intake form → auto-generates lead previews")
    server.serve_forever()
