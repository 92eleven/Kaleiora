# Kaleiora Agentic Marketing — Setup Guide

## Overview
Kaleiora runs entirely in mock mode with no API keys configured. You can demo the full system immediately.
When you're ready to go live, add your API keys to `config/api_keys.json` — no code changes needed.

## Step 1: Run in Mock Mode (Zero Config)
1. Ensure Python 3.8+ is installed
2. Start the dashboard: `python3 dashboard_server.py`
3. Open `http://localhost:8000` in your browser
4. The system runs in mock mode — every feature works, all output labeled MOCK - NOT LIVE

## Step 2: Get Your API Keys

| Integration | Purpose | Cost | Where to Get It |
|------------|---------|------|-----------------|
| Ideogram | AI image generation | ~$20/mo | https://ideogram.ai/api |
| Cloudinary | Product image + text overlay | Free tier | https://cloudinary.com/console |
| Make.com | Social media scheduling | Free tier / $9/mo | https://make.com |
| SendGrid | Email campaign deployment | Free tier (100/day) | https://sendgrid.com |
| Slack | Crisis alerts | Free | https://api.slack.com/messaging/webhooks |
| Runway ML | AI video generation | $12/mo | https://runwayml.com |
| InVideo AI | AI video generation | $17/mo | https://invideo.io |

## Step 3: Enter Keys in config/api_keys.json
Open `config/api_keys.json` and add your keys:
```json
{
  "integrations": {
    "ideogram": { "api_key": "your-key", "enabled": true },
    "cloudinary": { "cloud_name": "your-name", "api_key": "your-key", "api_secret": "your-secret", "enabled": true },
    "makecom": { "webhook_url": "https://...", "enabled": true },
    "sendgrid": { "api_key": "your-key", "enabled": true },
    "slack": { "webhook_url": "https://...", "enabled": true }
  }
}
```

## Step 4: Verify Live Mode
1. Restart the dashboard server
2. Check the Integration Status panel on the dashboard
3. All configured integrations show 🟢 LIVE
4. Empty integrations still show 🟡 MOCK MODE
5. Run a test campaign — integrations use live APIs

## File Structure
```
config/api_keys.json        ← Your API keys (never hardcoded)
scripts/quality_gate.py     ← Real validation engine
scripts/red_line_protocol.py ← Functional crisis management
scripts/ideogram_client.py  ← Image generation (mock/live)
scripts/cloudinary_client.py ← Image composition (mock/live)
scripts/makecom_client.py   ← Social scheduling (mock/live)
scripts/sendgrid_client.py  ← Email deployment (mock/live)
scripts/slack_connector.py  ← Slack alerts (mock/live)
scripts/config_loader.py    ← Reads all keys at runtime
command_center.html         ← Live dashboard with all panels
```

## Troubleshooting
- **Dashboard won't load**: Run `python3 dashboard_server.py` from the repo root
- **Integrations show MOCK**: Check `config/api_keys.json` has the key and `enabled: true`
- **Red-Line won't clear**: Run the recovery function with a valid asset
- **Quality Gate rejecting everything**: Check asset text against client brand DNA in Vector DB
