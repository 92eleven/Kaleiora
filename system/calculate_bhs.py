import json
import os

# Define standard paths
METRICS_PATH = '/home/team/shared/performance_metrics.json'

def calculate_bhs(roas_actual=None, roas_target=None, cac_actual=None, cac_target=None, alignment=90, velocity=80, sentiment=85, client_id=None):
    """
    Calculates the Brand Health Score. 
    Can either take values directly or fetch them from performance_metrics.json if client_id is provided.
    """
    
    # If client_id is provided, prioritize fetching from performance_metrics.json
    if client_id and os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, 'r') as f:
                all_metrics = json.load(f)
            if client_id in all_metrics:
                m = all_metrics[client_id]
                roas_actual = m.get('roas', {}).get('actual', roas_actual)
                roas_target = m.get('roas', {}).get('target', roas_target)
                cac_actual = m.get('cac', {}).get('actual', cac_actual)
                cac_target = m.get('cac', {}).get('target', cac_target)
        except Exception as e:
            print(f"Error reading metrics for {client_id}: {e}")

    # Fallbacks/Defaults if still None
    roas_actual = roas_actual if roas_actual is not None else 4.0
    roas_target = roas_target if roas_target is not None else 5.0
    cac_actual = cac_actual if cac_actual is not None else 40.0
    cac_target = cac_target if cac_target is not None else 30.0
    
    # ROAS Score (25%)
    roas_score = min((roas_actual / roas_target) * 100, 120) if roas_target > 0 else 0
    
    # CAC Score (20%)
    cac_score = min((cac_target / cac_actual) * 100, 120) if cac_actual > 0 else 0
    
    weights = {
        "roas": 0.25,
        "cac": 0.20,
        "alignment": 0.25,
        "velocity": 0.15,
        "sentiment": 0.15
    }
    
    overall_score = (
        (roas_score * weights["roas"]) +
        (cac_score * weights["cac"]) +
        (alignment * weights["alignment"]) +
        (velocity * weights["velocity"]) +
        (sentiment * weights["sentiment"])
    )
    
    overall_score = round(overall_score)
    
    if overall_score >= 75:
        status = "OPTIMIZED"
        color = "Green"
    elif overall_score >= 50:
        status = "STABLE"
        color = "Yellow"
    else:
        status = "RED-LINE"
        color = "Red"
        
    return {
        "overall_score": overall_score,
        "status": status,
        "color": color,
        "client_id": client_id,
        "pillars": {
            "roas": {"score": round(roas_score), "actual": roas_actual, "target": roas_target},
            "cac": {"score": round(cac_score), "actual": cac_actual, "target": cac_target},
            "alignment": {"score": alignment, "actual": alignment, "target": 100},
            "velocity": {"score": velocity, "actual": velocity, "target": 100},
            "sentiment": {"score": sentiment, "actual": sentiment, "target": 100}
        }
    }

if __name__ == "__main__":
    # Example usage / Default values
    result = calculate_bhs(
        roas_actual=4.25,
        roas_target=5.0,
        cac_actual=45.0,
        cac_target=40.0,
        alignment=90,
        velocity=70,
        sentiment=85
    )
    print(json.dumps(result, indent=2))
