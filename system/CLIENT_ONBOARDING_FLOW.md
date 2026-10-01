# 🌟 Real Client Onboarding Flow — From Prospect to Campaign Live

## Step 1: Prospect Discovers Kaleiora
A founder/CMO lands on the Kaleiora Command Center.
They see a clean cyberpunk dashboard with a **"+ New Client Intake"** button.

![Dashboard screenshot - intake button]

**What they see:** Live agent status, brand health gauge, performance metrics.
**First impression:** "This is WAY more transparent than any agency I've worked with."

---

## Step 2: They Fill Out the Intake Form
They click the button → a modal form opens with 3 fields:

```
Client Name: _______________
Brand Guidelines (URL or text): _______________
Primary KPI: [ROAS ▼]
```

They paste their brand info and hit **"Initialize Client Onboarding"**

---

## Step 3: The Swarm Responds (instantly)

### T+0 seconds — Lead Preview Engine fires
The intake form saves → `generate_lead_preview.py` detects the file
→ Auto-detects their industry from their brand text
→ Generates a **beautiful HTML sneak peek** with:
  - A sample social media post written in their brand voice
  - Sample ad copy tailored to their industry
  - Their brand name, industry tone, and a "Want the full campaign?" CTA

**The prospect sees:** A link to their preview page — personalized marketing copy
**Their reaction:** "They generated this for me in seconds??"

### T+5 seconds — Auto-Onboarding Pipeline fires
`auto_onboarding.py` detects the intake file
→ Ingests their brand guidelines into the Vector DB
→ Sets them as an **Active** client
→ Seeds baseline performance metrics
→ Moves the intake file to `processed_intakes/`

**System state:** New client live in Vector DB, ready for campaigns

### T+30 seconds — Creative Agent is triggered (if they opt in)
`generate_novatech_campaign.py` reads their brand DNA from Vector DB
→ Generates a full campaign: LinkedIn post, Instagram, ad copy, email, landing page
→ Every piece uses their do_say phrases, avoids their dont_say terms
→ Uses their brand colors and visual style (via Runway/Canva when keys are live)

### T+60 seconds — Quality Gate validates everything
Brand Custodian runs `client_vector_db.sh validate` on each asset
→ Only on-brand assets pass through
→ Audit logged with timestamps
→ Violations blocked — never reach the client

### T+90 seconds — Dashboard updates in real-time
`sync_bhs.py` updates the Brand Health Score
→ New assets appear in the "Creative Assets" panel
→ Daily digest auto-updates
→ If Red-Line triggers, campaigns auto-pause (kill switch)

---

## Step 4: The Prospect Sees Results

**Immediately:** A personalized "Sneak Peek" HTML page they can view in their browser
**Within minutes:** A full campaign ready for review
**Daily:** An auto-generated performance digest showing BHS, ROAS, CAC, agent activity
**On crisis:** Auto-pause + Slack alert + Red-Line recovery

---

## What You Do vs What the Swarm Does

| You | The Swarm |
|-----|-----------|
| Share the dashboard link | Generates the lead preview |
| Get the API key (Runway/Canva) | Onboards the client into Vector DB |
| Tell them "yes, go" | Creates full campaign from brand DNA |
| Collect the revenue | Validates via Quality Gate |
| | Updates dashboard in real-time |
| | Auto-recovers from any crisis |

---

## The Sales Pitch

When a prospect hesitates, send them this:

> *"Fill out the 30-second form on our dashboard. In under a minute, you'll have a personalized sample of what your marketing looks like with AI swarm automation — a social post, ad copy, and brand treatment written specifically for YOUR business. No commitment. Just proof."*

Then the system does the rest.