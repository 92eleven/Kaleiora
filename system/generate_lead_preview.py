#!/usr/bin/env python3
"""
Kaleiora Agentic Marketing - Lead Conversion Sneak Peek Engine
===============================================================
When a prospect submits the intake form, this generates a sample
marketing asset showing what Kaleiora can do for THEIR brand.

FLOW:
  Prospect fills intake form → intake_<name>.json saved
  → generate_lead_preview.py reads it
  → Creates sample social post + ad copy + graphic concept
  → Saves as HTML preview in /home/team/shared/lead_previews/
  → Dashboard shows link: "See your brand's sneak peek →"

CONVERSION GOAL: Show prospects a real sample before they commit.
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path

INTAKE_DIR = "/home/team/shared"
PREVIEW_DIR = "/home/team/shared/lead_previews"
DASHBOARD_FILE = "/home/team/shared/dashboard_data.json"

# Industry tone templates - infers brand voice from industry keywords
INDUSTRY_TONE_MAP = {
    "saas": {"voice": "Confident, direct, solution-focused", "hashtags": ["#SaaS", "#Innovation", "#Productivity"]},
    "ai": {"voice": "Forward-thinking, accessible, empowering", "hashtags": ["#AI", "#SmartAutomation", "#FutureOfWork"]},
    "tech": {"voice": "Innovative, precise, forward-looking", "hashtags": ["#Tech", "#Innovation", "#DigitalTransformation"]},
    "finance": {"voice": "Trustworthy, authoritative, clear", "hashtags": ["#Finance", "#SmartMoney", "#FinancialFreedom"]},
    "healthcare": {"voice": "Compassionate, professional, reliable", "hashtags": ["#Healthcare", "#Wellness", "#PatientCare"]},
    "retail": {"voice": "Engaging, trend-aware, customer-first", "hashtags": ["#Retail", "#Shopping", "#CustomerFirst"]},
    "food": {"voice": "Warm, authentic, community-focused", "hashtags": ["#Food", "#Fresh", "#TasteTheDifference"]},
    "fitness": {"voice": "Energetic, motivational, results-driven", "hashtags": ["#Fitness", "#Health", "#GetStronger"]},
    "education": {"voice": "Inspiring, knowledgeable, supportive", "hashtags": ["#Education", "#Learning", "#Growth"]},
    "realestate": {"voice": "Trustworthy, aspirational, local-focused", "hashtags": ["#RealEstate", "#Home", "#Property"]},
    "beauty": {"voice": "Elegant, aspirational, authentic", "hashtags": ["#Beauty", "#Skincare", "#NaturalBeauty"]},
    "wellness": {"voice": "Holistic, nurturing, trustworthy", "hashtags": ["#Wellness", "#SelfCare", "#HealthyLiving"]},
    "default": {"voice": "Professional, engaging, results-focused", "hashtags": ["#Business", "#Growth", "#Success"]},
}


def detect_industry(intake_data):
    """Detect industry from intake form fields."""
    text = json.dumps(intake_data).lower()
    for keyword in INDUSTRY_TONE_MAP:
        if keyword in text:
            return keyword
    # Try matching industry-related words
    industries = {
        "saas": ["software", "cloud", "platform", "app", "digital"],
        "ai": ["artificial intelligence", "machine learning", "automation", "data science"],
        "tech": ["technology", "startup", "innovation", "engineering"],
        "finance": ["banking", "accounting", "fintech", "invest", "money", "financial"],
        "healthcare": ["health", "medical", "clinic", "patient", "wellness"],
        "retail": ["store", "ecommerce", "shop", "product", "merchant"],
        "food": ["restaurant", "organic", "food", "meal", "grocery", "farm"],
        "fitness": ["gym", "workout", "fitness", "wellness", "training"],
        "education": ["school", "university", "course", "learning", "student", "training"],
        "realestate": ["property", "home", "apartment", "real estate", "mortgage"],
    }
    for industry, keywords in industries.items():
        for kw in keywords:
            if kw in text:
                return industry
    return "default"


def infer_brand_name(intake_data):
    """Extract or generate a brand name from intake data."""
    name = intake_data.get("client_name", "")
    if name:
        return name
    # Try to find any name-like field
    for field in ["business_name", "company", "brand", "name"]:
        val = intake_data.get(field, "")
        if val:
            return val
    return "Your Brand"


def generate_sample_copy(brand_name, industry_tone, intake_data=None):
    """Generate a sample social post and ad copy using intake data."""
    voice = industry_tone["voice"]
    hashtags = " ".join(industry_tone["hashtags"])

    # Extract personalized fields from intake data
    competitors = intake_data.get("competitors", "") if intake_data else ""
    target_audience = intake_data.get("target_audience", "") if intake_data else ""
    pain_point = intake_data.get("pain_point", "") if intake_data else ""
    social_channel = intake_data.get("social_channel", "") if intake_data else ""

    # Pain-point specific hooks
    pain_hooks = {
        "brand_awareness": "Nobody knows you exist yet — but they should.",
        "social_media": f"Your {social_channel or 'social media'} should be your growth engine, not a ghost town.",
        "content_creation": "You know you need more content. The question is how to produce it without burning out.",
        "conversions": "Traffic without sales isn't a win — it's a leak in the bucket.",
        "consistency": "Your brand voice changes every post. Your customers notice.",
        "roi": "You're spending on marketing but can't connect the dots to revenue.",
    }
    hook = pain_hooks.get(pain_point, "Your audience is ready. Are you giving them a reason to stop scrolling?")

    # Build competitor reference
    comp_text = ""
    if competitors:
        comps = [c.strip() for c in competitors.split(",") if c.strip()]
        if len(comps) >= 3:
            comp_text = f"While {comps[0]}, {comps[1]}, and {comps[2]} compete for attention with the same playbook, {brand_name} has something they don't: a message that actually connects."
        elif len(comps) == 2:
            comp_text = f"{comps[0]} and {comps[1]} aren't your problem. Blending in with them is."
        elif len(comps) == 1:
            comp_text = f"You're not here to copy {comps[0]}. You're here to outthink them."

    # Audience reference
    aud_text = ""
    if target_audience:
        aud_text = f"We're talking to {target_audience.lower().strip('.')} — and we know exactly what they need to hear."

    social_post = (
        f"✨ **Sneak Peek for {brand_name}** ✨\n\n"
        f"{hook}\n\n"
        f"{comp_text + ' ' if comp_text else ''}"
        f"{aud_text + ' ' if aud_text else ''}"
        f"With a {voice} approach, every piece of content becomes a connection.\n\n"
        f"Your customers aren't looking for more noise. "
        f"They're looking for the brand that understands them.\n\n"
        f"Let's make sure that brand is you.\n\n"
        f"{hashtags}\n#KaleioraAgentic"
    )

    ad_copy = (
        f"**Headline:** {brand_name} — The Message They've Been Waiting For\n\n"
        f"**Body:**\n"
        f"{hook}\n\n"
        f"{comp_text + chr(10) + chr(10) if comp_text else ''}"
        f"{aud_text + chr(10) + chr(10) if aud_text else ''}"
        f"With Kaleiora Agentic Marketing, {brand_name} gets:\n"
        f"✅ AI-powered creative tailored to your brand voice\n"
        f"{"✅ Social content optimized for " + social_channel.title() + "\n" if social_channel else ""}"
        f"✅ Campaigns that adapt in real-time\n"
        f"✅ A live dashboard showing exactly what's working\n\n"
        f"From prospect to loyal customer — faster than you thought possible.\n\n"
        f"**CTA:** See what {brand_name} looks like with agentic marketing."
    )

    return social_post, ad_copy


def create_html_preview(brand_name, social_post, ad_copy, intake_data):
    """Create a beautiful HTML preview page for the lead."""
    preview_id = f"preview-{uuid.uuid4().hex[:8]}"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kaleiora Sneak Peek — {brand_name}</title>
    <style>
        :root {{
            --bg: #0a0a0b;
            --card: #141417;
            --border: #2a2a30;
            --text: #e0e0e0;
            --muted: #909090;
            --accent: #00f2ff;
            --success: #00ff88;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: 'Courier New', monospace;
            padding: 2rem;
            max-width: 800px;
            margin: 0 auto;
        }}
        .logo {{
            font-size: 1.5rem;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 2rem;
            text-shadow: 0 0 10px rgba(0,242,255,0.5);
        }}
        .badge {{
            display: inline-block;
            background: rgba(0,255,136,0.1);
            color: var(--success);
            border: 1px solid var(--success);
            padding: 4px 12px;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 1rem;
        }}
        .hero {{
            padding: 2rem 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 2rem;
        }}
        .hero h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        .hero p {{
            color: var(--muted);
            font-size: 0.9rem;
        }}
        .card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        .card h2 {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--muted);
            margin-bottom: 1rem;
        }}
        .card .content {{
            white-space: pre-wrap;
            font-size: 0.85rem;
            line-height: 1.6;
            color: var(--text);
        }}
        .cta-box {{
            background: rgba(0,242,255,0.05);
            border: 1px solid var(--accent);
            border-radius: 4px;
            padding: 1.5rem;
            text-align: center;
            margin-top: 2rem;
        }}
        .cta-box h3 {{
            color: var(--accent);
            margin-bottom: 0.5rem;
        }}
        .cta-box p {{
            color: var(--muted);
            font-size: 0.85rem;
        }}
        .meta {{
            text-align: center;
            color: var(--muted);
            font-size: 0.7rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        .info-item {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 1rem;
        }}
        .info-item .label {{
            font-size: 0.7rem;
            color: var(--muted);
            text-transform: uppercase;
        }}
        .info-item .value {{
            font-size: 0.85rem;
            margin-top: 0.25rem;
        }}
    </style>
</head>
<body>
    <div class="logo">⬡ Kaleiora</div>
    <div class="badge">⚡ Sneak Peek — Generated for {brand_name}</div>

    <div class="hero">
        <h1>Your Brand, Amplified ✨</h1>
        <p>Here's a preview of how Kaleiora Agentic Marketing would craft your message.
        This sample was generated automatically from your intake information.</p>
    </div>

    <div class="info-grid">
        <div class="info-item">
            <div class="label">Brand</div>
            <div class="value">{brand_name}</div>
        </div>
        <div class="info-item">
            <div class="label">Generated</div>
            <div class="value">{timestamp}</div>
        </div>
        <div class="info-item">
            <div class="label">Industry Tone</div>
            <div class="value">{detect_industry(intake_data).title()}</div>
        </div>
        <div class="info-item">
            <div class="label">Campaign Type</div>
            <div class="value">Social + Paid Media</div>
        </div>
    </div>

    <div class="card">
        <h2>📱 Social Media Post</h2>
        <div class="content">{social_post}</div>
    </div>

    <div class="card">
        <h2>📢 Paid Ad Copy</h2>
        <div class="content">{ad_copy}</div>
    </div>

    <div class="cta-box">
        <h3>🚀 Want the Full Campaign?</h3>
        <p>This was generated in seconds from your intake form. Imagine what a full
        agentic campaign — with Quality Gate validation, real-time dashboard tracking,
        and autonomous optimization — could do for {brand_name}.</p>
        <p style="margin-top: 1rem; color: var(--success);">
        → Complete your onboarding to unlock the full Kaleiora swarm.
        </p>
    </div>

    <div class="meta">
        Kaleiora Agentic Marketing — AI-Powered. Human-Guided. Results-Driven.
    </div>
</body>
</html>"""

    output_path = os.path.join(PREVIEW_DIR, f"{preview_id}.html")
    with open(output_path, 'w') as f:
        f.write(html)

    return output_path, preview_id


def process_intake(intake_file):
    """Process a single intake file and generate a preview."""
    try:
        with open(intake_file, 'r') as f:
            intake_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return None, f"Error reading intake: {e}"

    brand_name = infer_brand_name(intake_data)
    industry = detect_industry(intake_data)
    tone = INDUSTRY_TONE_MAP.get(industry, INDUSTRY_TONE_MAP["default"])

    social_post, ad_copy = generate_sample_copy(brand_name, tone, intake_data)
    preview_path, preview_id = create_html_preview(brand_name, social_post, ad_copy, intake_data)

    # Log to dashboard
    try:
        with open(DASHBOARD_FILE, 'r') as f:
            dashboard = json.load(f)
        leads = dashboard.get("leads", [])
        lead_entry = {
            "id": preview_id,
            "brand": brand_name,
            "industry": industry,
            "preview": f"/lead_previews/{preview_id}.html",
            "generated_at": datetime.utcnow().isoformat(),
            "status": "preview_generated"
        }
        # Check if this lead already exists
        existing = [l for l in leads if l.get("brand") == brand_name]
        if not existing:
            leads.append(lead_entry)
        dashboard["leads"] = leads
        # Update the digest
        dashboard["daily_digest"] = (
            f"⚡ New lead preview generated for {brand_name} "
            f"({industry.title()}) — sneak peek ready at lead_previews/{preview_id}.html"
        )
        with open(DASHBOARD_FILE, 'w') as f:
            json.dump(dashboard, f, indent=2)
    except:
        pass

    return preview_path, {
        "brand": brand_name,
        "industry": industry,
        "preview_id": preview_id,
        "assets": {
            "social_post": social_post[:100] + "...",
            "ad_copy": ad_copy[:100] + "...",
        }
    }


def watch_for_intakes():
    """Watch for new intake files and auto-generate previews."""
    print("⬡ Kaleiora Lead Preview Engine — Watching for new intakes...")
    processed = set()
    while True:
        for fname in os.listdir(INTAKE_DIR):
            if fname.startswith("intake_") and fname.endswith(".json"):
                fpath = os.path.join(INTAKE_DIR, fname)
                if fpath not in processed:
                    processed.add(fpath)
                    print(f"\n⚡ New lead detected: {fname}")
                    preview_path, info = process_intake(fpath)
                    if preview_path:
                        print(f"   ✅ Preview generated: {preview_path}")
                        print(f"   Brand: {info['brand']} | Industry: {info['industry']}")
                    else:
                        print(f"   ❌ Error: {info}")
        import time
        time.sleep(5)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        watch_for_intakes()
    elif len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
        path, info = process_intake(sys.argv[1])
        if path:
            print(f"✅ Preview saved: {path}")
            print(json.dumps(info, indent=2))
        else:
            print(f"❌ {info}")
    else:
        # Demo — create a sample lead and generate preview
        sample_lead = {
            "client_name": "demo-brand",
            "brand_guidelines": "A premium organic skincare company focused on sustainability and natural ingredients. Target audience: health-conscious women 25-45.",
            "kpi": "brand_awareness"
        }
        sample_path = f"{INTAKE_DIR}/intake_demo_lead.json"
        with open(sample_path, 'w') as f:
            json.dump(sample_lead, f, indent=2)
        print(f"📝 Created sample lead: {sample_path}")
        path, info = process_intake(sample_path)
        if path:
            print(f"✅ Preview saved: {path}")
            print(json.dumps(info, indent=2))
