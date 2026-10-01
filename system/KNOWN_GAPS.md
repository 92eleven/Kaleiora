# Known Gaps — Kaleiora Agentic Marketing

This file documents features that are architecturally designed and code-ready
but require external services or additional implementation to be fully functional.

## 1. Live API Integrations (All in Mock Mode)
All external integrations run in mock mode when no API keys are configured.
They switch to live automatically when keys are added via config/api_keys.json.
- Ideogram: Needs IDEOGRAM_API_KEY → generates real images
- Cloudinary: Needs CLOUDINARY_API_KEY + CLOUDINARY_CLOUD_NAME + CLOUDINARY_API_SECRET → real image uploads
- Make.com: Needs MAKECOM_WEBHOOK_URL → real social scheduling
- SendGrid: Needs SENDGRID_API_KEY → real email delivery
- Slack: Needs SLACK_WEBHOOK_URL → real alerts

## 2. Retry & Escalation (Quality Gate)
The 3-retry cycle for Quality Gate failures escalating to Red-Line is
designed in the architecture but the retry orchestrator loop is not yet
built. Creative Agent would need to be invoked to generate revised assets.
Suggested fix: Build a campaign_orchestrator.py that manages the retry loop.

## 3. Full Campaign Orchestration
The individual components (Quality Gate, Red-Line, Ideogram, SendGrid, Make.com)
all work independently. The end-to-end campaign orchestrator that ties them
together as a single pipeline is not yet built. The existing
orchestrate_campaign_cycle.py covers the basic flow but doesn't include
the new integrations. Suggested fix: Update orchestrate_campaign_cycle.py
to call Ideogram for images, Cloudinary for compositions, Make.com for
distribution, and SendGrid for email deployment.

## 4. Real BHS Monitoring Integration
The Red-Line auto-trigger works but needs to be wired into the BHS calculation
loop. Currently it must be called manually or via the monitor_bhs.py script.
Suggested fix: Integrate red_line_protocol.trigger() into the sync_bhs.py loop
so it fires automatically when BHS drops below 50.
