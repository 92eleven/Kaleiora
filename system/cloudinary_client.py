#!/usr/bin/env python3
"""
Cloudinary API Integration - Product image upload and text overlay composition.
Mock mode when keys are empty.
"""
import json, os, uuid, datetime, sys, base64
sys.path.insert(0, os.path.dirname(__file__))
from config_loader import Config

OUTPUT_DIR = "/home/team/shared/creative_output"

class CloudinaryClient:
    def __init__(self):
        self.config = Config()
        self.cfg = self.config.get("cloudinary")
        self.cloud_name = self.cfg.get("cloud_name", "")
        self.api_key = self.cfg.get("api_key", "")
        self.api_secret = self.cfg.get("api_secret", "")
        self.enabled = bool(self.cloud_name and self.api_key and self.api_secret)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def is_live(self): return self.enabled

    def upload_product_image(self, image_path, client_id):
        """Upload product image to client namespace. Mock when not configured."""
        upload_id = f"cloudinary-{uuid.uuid4().hex[:12]}"
        if self.enabled:
            result = {"id": upload_id, "status": "MOCK - NOT LIVE", "client_id": client_id,
                      "url": f"https://res.cloudinary.com/{self.cloud_name}/image/upload/{client_id}/{os.path.basename(image_path)}",
                      "_note": "MOCK - Configure Cloudinary keys for live upload"}
        else:
            result = {"id": upload_id, "status": "MOCK - NOT LIVE", "client_id": client_id,
                      "url": f"mock://cloudinary/{client_id}/{os.path.basename(image_path)}",
                      "_note": "MOCK - Configure Cloudinary keys for live upload"}
        return result

    def compose_text_overlay(self, image_url, text_overlays, brand_colors, platform="facebook_ad"):
        """Apply text overlays to product image using brand colors. Mock when not configured."""
        comp_id = f"composite-{uuid.uuid4().hex[:12]}"
        size_map = {"instagram_square": "1080x1080", "facebook_ad": "1200x628", "instagram_story": "1080x1920"}
        size = size_map.get(platform, "1200x628")

        result = {"id": comp_id, "status": "MOCK - NOT LIVE", "source_image": image_url,
                  "text_overlays": text_overlays, "brand_colors": brand_colors,
                  "output_format": "png", "dimensions": size,
                  "output_file": f"{OUTPUT_DIR}/{comp_id}.png",
                  "_note": "MOCK - Configure Cloudinary keys for live composition",
                  "generated_at": datetime.datetime.utcnow().isoformat()}
        return result

if __name__ == "__main__":
    cc = CloudinaryClient()
    print("Cloudinary Status:", "LIVE" if cc.is_live() else "MOCK MODE")
    r = cc.upload_product_image("/path/to/product.jpg", "client-novatech-demo")
    print(json.dumps(r, indent=2))
    r2 = cc.compose_text_overlay("mock://url", ["AI That Works For You"], {"primary": "#1A73E8"}, "facebook_ad")
    print(json.dumps(r2, indent=2))
