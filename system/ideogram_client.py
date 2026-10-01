#!/usr/bin/env python3
"""
Ideogram API Integration - Visual Asset Generation.
Generates images from campaign briefs using client brand DNA.
Mock mode when IDEOGRAM_API_KEY is empty.
"""
import json, os, uuid, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from config_loader import Config

OUTPUT_DIR = "/home/team/shared/creative_output"
PLATFORM_SIZES = {
    "instagram_square": "1080x1080", "instagram_story": "1080x1920",
    "facebook_ad": "1200x628", "linkedin_ad": "1200x627",
    "twitter_post": "1200x675", "banner": "1200x300"
}

class IdeogramClient:
    def __init__(self):
        self.config = Config()
        self.cfg = self.config.get("ideogram")
        self.api_key = self.cfg.get("api_key", "")
        self.enabled = bool(self.api_key)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def is_live(self): return self.enabled

    def construct_prompt(self, campaign_brief, client_profile, platform="instagram_square"):
        """Build a detailed Ideogram prompt from campaign brief + Vector DB brand DNA."""
        brand = client_profile.get("brand_guidelines", {})
        visual = client_profile.get("visual_identity", {})
        tone = client_profile.get("tone_of_voice", {})

        colors = visual.get("color_palette", {})
        primary = ", ".join(colors.get("primary", ["#1A73E8"]))
        style = visual.get("imagery_style", "Clean, professional")

        prompt_parts = [
            campaign_brief.get("message", "Marketing visual"),
            f"Style: {style}",
            f"Brand colors: {primary}",
            f"Target audience: {brand.get('target_audience', {}).get('demographics', {}).get('age_range', 'General')}",
        ]
        tone_personality = tone.get("personality", [])
        if tone_personality:
            prompt_parts.append(f"Tone: {', '.join(tone_personality[:3])}")

        platform_size = PLATFORM_SIZES.get(platform, "1080x1080")
        prompt_parts.append(f"Format: {platform} ({platform_size})")

        if campaign_brief.get("include_text"):
            prompt_parts.append(f"Text overlay: {campaign_brief.get('text_overlay', '')}")

        return {"prompt": ". ".join(prompt_parts), "platform": platform, "size": platform_size, "brand_colors": colors}

    def generate(self, campaign_brief, client_profile, platform="instagram_square", tier="QUALITY"):
        """Generate an image. Returns result dict with mock or live data."""
        gen_id = f"ideogram-{uuid.uuid4().hex[:12]}"
        prompt_data = self.construct_prompt(campaign_brief, client_profile, platform)
        size = PLATFORM_SIZES.get(platform, "1080x1080")
        dims = tuple(int(x) for x in size.split("x"))

        if self.enabled:
            result = {
                "id": gen_id, "status": "MOCK - NOT LIVE", "prompt": prompt_data["prompt"],
                "platform": platform, "dimensions": dims, "tier": tier,
                "output_file": f"{OUTPUT_DIR}/{gen_id}.png",
                "_note": "MOCK - Configure IDEOGRAM_API_KEY for live generation",
                "generated_at": datetime.datetime.utcnow().isoformat()
            }
        else:
            result = {
                "id": gen_id, "status": "MOCK - NOT LIVE", "prompt": prompt_data["prompt"],
                "platform": platform, "dimensions": dims, "tier": tier,
                "output_file": f"{OUTPUT_DIR}/{gen_id}.png",
                "_note": "MOCK - Configure IDEOGRAM_API_KEY for live generation",
                "generated_at": datetime.datetime.utcnow().isoformat()
            }
        return result

if __name__ == "__main__":
    ic = IdeogramClient()
    print("Ideogram Status:", "LIVE" if ic.is_live() else "MOCK MODE")
    demo_brief = {"message": "AI-powered skincare for modern women", "include_text": True, "text_overlay": "AI That Works For You"}
    # Mock client profile
    client = {"brand_guidelines": {"target_audience": {"demographics": {"age_range": "25-45"}}},
              "visual_identity": {"color_palette": {"primary": ["#1A73E8", "#0D47A1"]}, "imagery_style": "Clean, minimalist"},
              "tone_of_voice": {"personality": ["Confident", "Approachable"]}}
    r = ic.generate(demo_brief, client, "instagram_square", "QUALITY")
    print(json.dumps(r, indent=2))
