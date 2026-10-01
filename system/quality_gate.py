#!/usr/bin/env python3
"""
Kaleiora Agentic Marketing - Quality Gate Engine
=================================================
Real validation engine that runs on every asset before approval.
Checks brand voice, audience alignment, competitor compliance,
platform compliance, and for visual assets: collision detection,
text safe zones, dimensions, font sizes, and color contrast.

Returns structured JSON pass/fail with blocking issues.
"""
import json, os, math, re
from datetime import datetime

DB_PATH = "/home/team/shared/client_vector_db.json"
PLATFORM_SPECS = {
    "instagram_square": {"width": 1080, "height": 1080, "min_font": 12},
    "instagram_story": {"width": 1080, "height": 1920, "min_font": 14},
    "facebook_ad": {"width": 1200, "height": 628, "min_font": 12},
    "linkedin_ad": {"width": 1200, "height": 627, "min_font": 12},
    "twitter_post": {"width": 1200, "height": 675, "min_font": 12},
    "email": {"width": 600, "height": None, "min_font": 14},
    "landing_page": {"width": 1200, "height": None, "min_font": 16},
}

# Simple contrast ratio calculator
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(r, g, b):
    rs = r/255.0; gs = g/255.0; bs = b/255.0
    rs = rs/12.92 if rs <= 0.03928 else ((rs+0.055)/1.055)**2.4
    gs = gs/12.92 if gs <= 0.03928 else ((gs+0.055)/1.055)**2.4
    bs = bs/12.92 if bs <= 0.03928 else ((bs+0.055)/1.055)**2.4
    return 0.2126*rs + 0.7152*gs + 0.0722*bs

def contrast_ratio(color1, color2):
    l1 = relative_luminance(*hex_to_rgb(color1))
    l2 = relative_luminance(*hex_to_rgb(color2))
    lighter = max(l1, l2); darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def load_client_db(client_id):
    try:
        with open(DB_PATH) as f:
            db = json.load(f)
        return db.get("clients", {}).get(client_id, {})
    except: return {}

def load_vector_db():
    try:
        with open(DB_PATH) as f:
            return json.load(f)
    except: return {"clients": {}}

def check_brand_voice(asset_text, client_profile):
    """Score 0-100 how well asset matches brand voice from Vector DB."""
    tone = client_profile.get("tone_of_voice", {})
    brand = client_profile.get("brand_guidelines", {})
    do_say = [d.lower() for d in tone.get("do_say", [])]
    dont_say = [d.lower() for d in tone.get("dont_say", [])]
    preferred = [p.lower() for p in tone.get("vocabulary", {}).get("preferred_terms", [])]
    avoid = [a.lower() for a in tone.get("vocabulary", {}).get("avoid_terms", [])]
    key_msgs = [k.lower() for k in brand.get("key_messages", [])]

    text_lower = (asset_text or "").lower()
    score = 100; details = []; violations = []; passes = []

    # Check dont_say violations
    for phrase in dont_say:
        if phrase in text_lower:
            score -= 15
            violations.append(f"TONE VIOLATION: '{phrase}' is in dont_say list")
            details.append({"check": "dont_say", "result": "FAIL", "detail": f"Contains '{phrase}'"})

    # Check avoid_terms violations
    for term in avoid:
        if term in text_lower:
            score -= 10
            violations.append(f"VOCABULARY VIOLATION: '{term}' is in avoid_terms list")
            details.append({"check": "avoid_terms", "result": "FAIL", "detail": f"Contains '{term}'"})

    # Check do_say usage
    do_say_found = sum(1 for p in do_say if p in text_lower)
    if do_say and do_say_found < len(do_say) * 0.5:
        score -= 5
        details.append({"check": "do_say_usage", "result": "WARN", "detail": f"Only {do_say_found}/{len(do_say)} do_say phrases used"})
    else:
        details.append({"check": "do_say_usage", "result": "PASS", "detail": f"{do_say_found}/{len(do_say)} phrases used"})

    # Check preferred terms
    pref_found = sum(1 for p in preferred if p in text_lower)
    if preferred and pref_found < len(preferred) * 0.3:
        score -= 5
        details.append({"check": "preferred_terms", "result": "WARN", "detail": f"Only {pref_found}/{len(preferred)} preferred terms used"})
    else:
        details.append({"check": "preferred_terms", "result": "PASS", "detail": f"{pref_found}/{len(preferred)} terms used"})

    # Check key messages
    msg_found = sum(1 for m in key_msgs if m in text_lower)
    if msg_found > 0:
        passes.append(f"{msg_found} key messages reflected in asset")
        details.append({"check": "key_messages", "result": "PASS", "detail": f"{msg_found} messages found"})
    else:
        details.append({"check": "key_messages", "result": "WARN", "detail": "No key messages detected"})

    score = max(0, min(100, score))
    return {"score": score, "passed": score >= 70, "details": details, "violations": violations, "passes": passes}

def check_audience_alignment(asset_text, client_profile):
    """Verify asset mentions or targets the correct audience segment."""
    audience = client_profile.get("brand_guidelines", {}).get("target_audience", {})
    demographics = audience.get("demographics", {})
    psychographics = audience.get("psychographics", {})
    pain_points = audience.get("pain_points", [])
    aspirations = audience.get("aspirations", [])

    text_lower = (asset_text or "").lower()
    score = 100; details = []

    # Check pain points are addressed
    pain_found = sum(1 for p in pain_points if p.lower() in text_lower)
    if pain_points and pain_found == 0:
        score -= 15
        details.append({"check": "pain_points", "result": "WARN", "detail": "No pain points addressed"})
    else:
        details.append({"check": "pain_points", "result": "PASS", "detail": f"{pain_found} pain points addressed"})

    # Check aspirations are referenced
    asp_found = sum(1 for a in aspirations if a.lower() in text_lower)
    if aspirations and asp_found == 0:
        score -= 10
        details.append({"check": "aspirations", "result": "WARN", "detail": "No aspirations referenced"})
    else:
        details.append({"check": "aspirations", "result": "PASS", "detail": f"{asp_found} aspirations referenced"})

    score = max(0, min(100, score))
    return {"score": score, "passed": score >= 70, "details": details}

def check_competitor_compliance(asset_text, client_profile):
    """Check asset doesn't violate competitor rules."""
    brand = client_profile.get("brand_guidelines", {})
    competitors = brand.get("competitors", [])
    text_lower = (asset_text or "").lower()
    details = []
    violations = []
    for comp in competitors:
        if comp.lower() in text_lower:
            violations.append(f"Competitor '{comp}' mentioned - verify this is allowed")
            details.append({"check": f"competitor_{comp}", "result": "WARN", "detail": f"Competitor '{comp}' mentioned"})
    if not violations:
        details.append({"check": "competitors", "result": "PASS", "detail": "No competitor references found"})
    return {"score": 100 if not violations else 70, "passed": True, "details": details, "violations": violations}

def check_platform_compliance(asset_type, dimensions=None):
    """Verify asset meets platform specifications."""
    spec = PLATFORM_SPECS.get(asset_type)
    if not spec:
        return {"score": 100, "passed": True, "details": [{"check": "platform", "result": "PASS", "detail": f"No spec for {asset_type}, skipped"}]}
    details = []
    score = 100
    if dimensions and spec["width"]:
        w, h = dimensions
        if w != spec["width"] or h != spec["height"]:
            score -= 25
            details.append({"check": "dimensions", "result": "FAIL", "detail": f"Got {w}x{h}, expected {spec['width']}x{spec['height']}"})
        else:
            details.append({"check": "dimensions", "result": "PASS", "detail": f"{w}x{h} matches spec"})
    return {"score": score, "passed": score >= 70, "details": details}

def check_bounding_box_collision(elements):
    """Check every text/image element has non-overlapping zone."""
    if not elements:
        return {"score": 100, "passed": True, "details": [{"check": "collision", "result": "PASS", "detail": "No elements to check"}]}
    details = []
    for i, a in enumerate(elements):
        ax1, ay1, ax2, ay2 = a.get("x",0), a.get("y",0), a.get("x",0)+a.get("w",0), a.get("y",0)+a.get("h",0)
        for j, b in enumerate(elements):
            if i >= j: continue
            bx1, by1, bx2, by2 = b.get("x",0), b.get("y",0), b.get("x",0)+b.get("w",0), b.get("y",0)+b.get("h",0)
            if ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1:
                details.append({"check": "collision", "result": "FAIL", "detail": f"Element {i} collides with element {j}"})
    if not details:
        details.append({"check": "collision", "result": "PASS", "detail": f"No collisions among {len(elements)} elements"})
    score = 100 if all(d["result"] == "PASS" for d in details) else 0
    return {"score": score, "passed": score >= 70, "details": details}

def check_text_safe_zone(elements):
    """Verify no text element is within 20px of any image/shape boundary."""
    if not elements:
        return {"score": 100, "passed": True, "details": [{"check": "safe_zone", "result": "PASS", "detail": "No elements"}]}
    details = []
    text_els = [e for e in elements if e.get("type") == "text"]
    image_els = [e for e in elements if e.get("type") in ("image", "shape")]
    for t in text_els:
        tx1, ty1 = t.get("x",0), t.get("y",0)
        for img in image_els:
            ix1, iy1, ix2, iy2 = img.get("x",0), img.get("y",0), img.get("x",0)+img.get("w",0), img.get("y",0)+img.get("h",0)
            dist = min(abs(tx1 - ix2), abs(tx1 + t.get("w",0) - ix1), abs(ty1 - iy2), abs(ty1 + t.get("h",0) - iy1))
            if dist < 20:
                details.append({"check": "safe_zone", "result": "FAIL", "detail": f"Text element {t.get('id','?')} only {dist}px from image boundary (min 20px)"})
    if not details:
        details.append({"check": "safe_zone", "result": "PASS", "detail": "All text elements respect safe zones"})
    score = 100 if all(d["result"] == "PASS" for d in details) else 0
    return {"score": score, "passed": score >= 70, "details": details}

def check_font_size_minimum(elements, asset_type):
    """Fail if any text element is below minimum font size for platform."""
    spec = PLATFORM_SPECS.get(asset_type, {})
    min_font = spec.get("min_font", 12)
    if not elements:
        return {"score": 100, "passed": True, "details": [{"check": "font_size", "result": "PASS", "detail": "No text elements"}]}
    details = []
    for el in elements:
        if el.get("type") == "text":
            fs = el.get("font_size", 0)
            if fs < min_font:
                details.append({"check": "font_size", "result": "FAIL", "detail": f"Font size {fs}px below minimum {min_font}px"})
    if not details:
        details.append({"check": "font_size", "result": "PASS", "detail": f"All fonts meet minimum {min_font}px"})
    score = 100 if all(d["result"] == "PASS" for d in details) else 0
    return {"score": score, "passed": score >= 70, "details": details}

def check_color_contrast(elements):
    """Verify text has sufficient contrast against background."""
    if not elements:
        return {"score": 100, "passed": True, "details": [{"check": "contrast", "result": "PASS", "detail": "No elements"}]}
    details = []
    for el in elements:
        fg = el.get("color", "#000000")
        bg = el.get("background", "#FFFFFF")
        try:
            cr = contrast_ratio(fg, bg)
            if cr < 4.5:
                details.append({"check": "contrast", "result": "FAIL", "detail": f"Contrast ratio {cr:.1f}:1 below 4.5:1 minimum"})
            else:
                details.append({"check": "contrast", "result": "PASS", "detail": f"Contrast ratio {cr:.1f}:1 OK"})
        except:
            details.append({"check": "contrast", "result": "SKIP", "detail": "Could not parse colors"})
    score = 100 if all(d["result"] == "PASS" for d in details) else 0
    return {"score": score, "passed": score >= 70, "details": details}

def run_quality_gate(asset_text, client_id, asset_type="social", elements=None, dimensions=None):
    """
    Run full Quality Gate on an asset. Returns structured JSON result.
    This is the main entry point for all validation.
    """
    client_profile = load_client_db(client_id)
    if not client_profile:
        return {"overall_status": "FAIL", "error": f"Client {client_id} not found in Vector DB"}

    results = {}
    blocking_issues = []
    all_passed = True

    # 1. Brand Voice Score
    r1 = check_brand_voice(asset_text, client_profile)
    results["brand_voice"] = r1
    if not r1["passed"]:
        all_passed = False
        blocking_issues.extend(r1.get("violations", []))

    # 2. Audience Alignment
    r2 = check_audience_alignment(asset_text, client_profile)
    results["audience_alignment"] = r2
    if not r2["passed"]:
        all_passed = False

    # 3. Competitor Compliance
    r3 = check_competitor_compliance(asset_text, client_profile)
    results["competitor_compliance"] = r3

    # 4. Platform Compliance
    r4 = check_platform_compliance(asset_type, dimensions)
    results["platform_compliance"] = r4
    if not r4["passed"]:
        all_passed = False
        for d in r4["details"]:
            if d["result"] == "FAIL": blocking_issues.append(d["detail"])

    # Visual checks (if elements provided)
    if elements:
        r5 = check_bounding_box_collision(elements)
        results["collision_detection"] = r5
        if not r5["passed"]:
            all_passed = False
            for d in r5["details"]:
                if d["result"] == "FAIL": blocking_issues.append(d["detail"])

        r6 = check_text_safe_zone(elements)
        results["text_safe_zone"] = r6
        if not r6["passed"]:
            all_passed = False
            for d in r6["details"]:
                if d["result"] == "FAIL": blocking_issues.append(d["detail"])

        r7 = check_font_size_minimum(elements, asset_type)
        results["font_size_minimum"] = r7
        if not r7["passed"]:
            all_passed = False
            for d in r7["details"]:
                if d["result"] == "FAIL": blocking_issues.append(d["detail"])

        r8 = check_color_contrast(elements)
        results["color_contrast"] = r8
        if not r8["passed"]:
            all_passed = False
            for d in r8["details"]:
                if d["result"] == "FAIL": blocking_issues.append(d["detail"])

    # Calculate BHS impact
    voice_score = r1.get("score", 100)
    bhs_impact = round(voice_score * 0.35 + r2.get("score", 100) * 0.25 + r3.get("score", 100) * 0.15 + r4.get("score", 100) * 0.25)

    # Generate recommendations
    recommendations = []
    for check_name, result in results.items():
        for d in result.get("details", []):
            if d["result"] == "FAIL":
                recommendations.append(f"Fix {check_name}: {d['detail']}")
            elif d["result"] == "WARN":
                recommendations.append(f"Improve {check_name}: {d['detail']}")

    overall = "PASS" if all_passed else "FAIL"

    return {
        "overall_status": overall,
        "individual_check_results": results,
        "blocking_issues": blocking_issues[:10],
        "recommendations": recommendations[:10],
        "bhs_impact": bhs_impact,
        "passed": all_passed
    }

if __name__ == "__main__":
    # Demo test
    result = run_quality_gate(
        "Check out our revolutionary AI platform that uses deep learning to transform your business!",
        "client-novatech-solutions-demo",
        asset_type="facebook_ad",
        dimensions=(1200, 628),
        elements=[
            {"id": "headline", "type": "text", "x": 50, "y": 50, "w": 500, "h": 60, "font_size": 36, "color": "#1A73E8", "background": "#FFFFFF"},
            {"id": "image1", "type": "image", "x": 50, "y": 150, "w": 500, "h": 300},
        ]
    )
    print(json.dumps(result, indent=2))
