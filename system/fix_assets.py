#!/usr/bin/env python3
"""
Fix: Regenerate the missing LinkedIn Thought Leadership post 
(the instagram carousel overwrote it due to same 'social' type)
"""

import json
import os
from datetime import datetime, timezone

OUTPUT_DIR = "/home/team/shared/creative_output"
CLIENT_ID = "client-novatech-solutions-demo"
CAMPAIGN_NAME = "ai-that-works-for-you"
TIMESTAMP = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

# Generate LinkedIn Thought Leadership with unique type 'social_linkedin'
data = {
    "type": "social_linkedin",
    "title": "NovaTech Solutions — AI That Works For You (LinkedIn Thought Leadership)",
    "content": (
        "AI that works for you, not the other way around.\n\n"
        "That's the philosophy behind everything we build at NovaTech Solutions.\n\n"
        "We hear it every day from small business owners: \"AI feels like it's designed for "
        "enterprises with dedicated data science teams — not for us.\"\n\n"
        "So we built something different. Our no-code AI assistant gives you smart automation "
        "and real data insights — without the complexity. Your business data stays yours, always. "
        "We handle the complexity so you don't have to.\n\n"
        "Your data. Your control. Your insights.\n\n"
        "From setup to ROI in under 30 days. Enterprise-grade business intelligence at prices "
        "that make sense for growing businesses. No PhD required — AI that anyone can use.\n\n"
        "Start small, scale smart. See what NovaTech's AI assistant can do for your business."
    ),
    "platform": "LinkedIn",
    "cta": "Click the link in the comments to start your free trial — setup takes under 10 minutes",
    "client_id": CLIENT_ID,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "brand_alignment_notes": (
        "Uses all 4 do_say phrases: 'AI that works for you, not the other way around', "
        "'We handle the complexity so you don't have to', 'Your data. Your control. Your insights.', "
        "'Start small, scale smart'. Uses 4/5 preferred terms: AI assistant, Smart automation, "
        "Data insights, Business intelligence. No-code AI term used. "
        "Reflects all 4 key messages. Zero dont_say or avoid_terms violations."
    )
}

# Save with unique filename
filename = f"{CLIENT_ID}_{CAMPAIGN_NAME}_social_linkedin_{TIMESTAMP}.json"
filepath = os.path.join(OUTPUT_DIR, filename)
with open(filepath, 'w') as f:
    json.dump(data, f, indent=2)
print(f"✓ Saved: {filename}")

# Now also regenerate the Instagram carousel with a unique type
ig_data = {
    "type": "social_instagram",
    "title": "NovaTech Solutions — Instagram Carousel (5 slides)",
    "content": (
        "Slide 1: Tired of complicated AI tools? 🤖\n"
        "Meet NovaTech — your no-code AI assistant that actually works for you.\n\n"
        "Slide 2: We handle the complexity so you don't have to.\n"
        "Smart automation for your business — no PhD required.\n\n"
        "Slide 3: Your data. Your control. Your insights.\n"
        "All your business intelligence stays yours, always. 🔒\n\n"
        "Slide 4: From setup to ROI in under 30 days.\n"
        "Enterprise AI at small business prices.\n\n"
        "Slide 5: Start small, scale smart.\n"
        "Link in bio to start your free trial →"
    ),
    "platform": "Instagram",
    "cta": "Link in bio to start your free trial",
    "client_id": CLIENT_ID,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "brand_alignment_notes": (
        "Slides use all do_say phrases, preferred vocabulary terms (AI assistant, "
        "Smart automation, Business intelligence, No-code AI), key messages. Memorable "
        "and scannable for Instagram audience."
    )
}

filename2 = f"{CLIENT_ID}_{CAMPAIGN_NAME}_social_instagram_{TIMESTAMP}.json"
filepath2 = os.path.join(OUTPUT_DIR, filename2)
with open(filepath2, 'w') as f:
    json.dump(ig_data, f, indent=2)
print(f"✓ Saved: {filename2}")

# Now update the manifest
manifest_file = None
for f in os.listdir(OUTPUT_DIR):
    if "manifest" in f and "novatech" in f:
        manifest_file = f
        break

if manifest_file:
    manifest_path = os.path.join(OUTPUT_DIR, manifest_file)
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    # Replace the duplicate social entries with correct references
    manifest["assets"] = [
        {
            "type": "social_linkedin",
            "title": "NovaTech Solutions — AI That Works For You (LinkedIn Thought Leadership)",
            "platform": "LinkedIn",
            "file": filename,
            "brand_alignment_notes": data["brand_alignment_notes"]
        },
        {
            "type": "social_instagram",
            "title": "NovaTech Solutions — Instagram Carousel (5 slides)",
            "platform": "Instagram",
            "file": filename2,
            "brand_alignment_notes": ig_data["brand_alignment_notes"]
        },
        {
            "type": "email",
            "title": "NovaTech Solutions — Welcome Email Series (Email 1 of 3)",
            "platform": "Email",
            "file": f"{CLIENT_ID}_{CAMPAIGN_NAME}_email_{TIMESTAMP.split('_')[0]}_215319.json"
        },
        {
            "type": "landing",
            "title": "NovaTech Solutions — Landing Page (Hero + Features Section)",
            "platform": "Landing Page",
            "file": f"{CLIENT_ID}_{CAMPAIGN_NAME}_landing_{TIMESTAMP.split('_')[0]}_215319.json"
        },
        {
            "type": "ad",
            "title": "NovaTech Solutions — Paid Social Ad (Urgent / Limited Time)",
            "platform": "LinkedIn | Instagram | Facebook",
            "file": f"{CLIENT_ID}_{CAMPAIGN_NAME}_ad_{TIMESTAMP.split('_')[0]}_215319.json"
        },
        {
            "type": "video",
            "title": "NovaTech Solutions — Brand Video: 'AI That Works For You'",
            "platform": "Website | Social Media",
            "file": f"{CLIENT_ID}_{CAMPAIGN_NAME}_video_{TIMESTAMP.split('_')[0]}_215319.json"
        },
        {
            "type": "social_graphic",
            "title": "NovaTech Solutions — LinkedIn Banner Graphic",
            "platform": "LinkedIn",
            "file": f"{CLIENT_ID}_{CAMPAIGN_NAME}_graphic_linkedin_{TIMESTAMP.split('_')[0]}_215319.json"
        },
        {
            "type": "social_graphic",
            "title": "NovaTech Solutions — Instagram Story Graphic",
            "platform": "Instagram",
            "file": f"{CLIENT_ID}_{CAMPAIGN_NAME}_graphic_story_{TIMESTAMP.split('_')[0]}_215319.json"
        }
    ]
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"✓ Updated manifest: {manifest_file}")

print()
print(f"✅ All {len(os.listdir(OUTPUT_DIR)) - 1} assets in output directory (excluding generation_log.json and .py)")
