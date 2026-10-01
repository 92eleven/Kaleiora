# Kaleiora Agentic Marketing — Buyer Quickstart
## From Zero to First Campaign in Under 30 Minutes

### Minute 0-5: Setup
1. Ensure Python 3.8+ is installed: `python3 --version`
2. Start the dashboard: `cd /path/to/Kaleiora && python3 dashboard_server.py`
3. Open `http://localhost:8000` in your browser
4. You're running in mock mode — no API keys needed

### Minute 5-10: Explore the Dashboard
5. See the **Agency Status** panel at top — shows OPTIMIZED
6. See the **Integration Status** panel — all integrations show 🟡 MOCK MODE
7. See the **Quality Gate** panel — ready for asset validation
8. See the **Red-Line Log** — ready for crisis events

### Minute 10-20: Test the Full System
Test each component to verify it works:

**Test Quality Gate:**
```bash
python3 -c "from scripts.quality_gate import run_quality_gate; import json; r=run_quality_gate('Check out our AI platform', 'client-novatech-solutions-demo', 'facebook_ad', [(1200,628)], [{'id':'h1','type':'text','x':50,'y':50,'w':500,'h':60,'font_size':36,'color':'#1A73E8','background':'#FFFFFF'}]); print(json.dumps(r,indent=2))"
```

**Test Red-Line Protocol:**
```bash
python3 -c "from scripts.red_line_protocol import RedLineProtocol; rl=RedLineProtocol(); rl.trigger(30,'client-novatech-solutions-demo','Test'); print('Red-Line triggered! Check dashboard.')"
```

**Test Ideogram (mock):**
```bash
python3 -c "from scripts.ideogram_client import IdeogramClient; ic=IdeogramClient(); print(ic.generate({'message':'Test'},{},'instagram_square','QUALITY'))"
```

**Test SendGrid (mock):**
```bash
python3 -c "from scripts.sendgrid_client import SendGridClient; sc=SendGridClient(); sc.send_campaign('Kaleiora','m@k.com','Test','Preview','<p>Hi</p>',['c@t.com'],'TestClient')"
```

**Test Make.com (mock):**
```bash
python3 -c "from scripts.makecom_client import MakecomClient; mc=MakecomClient(); mc.schedule_post('NovaTech','post','/p/a.png','Caption',['#tag'],'linkedin','2026-06-10T10:00:00Z')"
```

### Minute 20-25: Add API Keys
Open `config/api_keys.json` and add any keys you have. The system auto-detects them.

### Minute 25-30: First Live Campaign
Once keys are configured, the Creative Agent can generate a full campaign
that goes through Quality Gate → Ideogram images → Make.com scheduling → SendGrid emails.

### Mock Mode Summary
Every feature works without API keys. All output is clearly labeled MOCK - NOT LIVE.
When you add keys, the system switches to live automatically. No code changes needed.

### Need Help?
- See SETUP_GUIDE.md for detailed API key setup
- Check config/api_keys.json for the integration slots
- Run any component's `__main__` block for a demo test
