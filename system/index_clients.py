#!/usr/bin/env python3
"""
Kaleiora Client Indexer — Generates per-client namespace files from the Vector DB.
Usage: python3 index_clients.py
Output: /home/team/shared/client_index/{client_id}.json per client
"""
import json
import os

DB_PATH = "/home/team/shared/client_vector_db.json"
INDEX_DIR = "/home/team/shared/client_index"

with open(DB_PATH) as f:
    db = json.load(f)

os.makedirs(INDEX_DIR, exist_ok=True)

clients = db.get("clients", {})

# Write per-client index files
for cid, cdata in clients.items():
    namespace = {
        "client_id": cid,
        "client_name": cdata.get("client_name", "Unknown"),
        "status": cdata.get("status", "unknown"),
        "created_at": cdata.get("created_at", ""),
        "brand_guidelines": cdata.get("brand_guidelines", {}),
        "tone_of_voice": cdata.get("tone_of_voice", {}),
        "visual_identity": cdata.get("visual_identity", {}),
        "validated_assets_count": len(cdata.get("validated_assets", [])),
        "campaigns_count": len(cdata.get("campaigns", [])),
        "validated_assets_summary": [
            {"asset_id": a.get("asset_id"), "title": a.get("title"), "type": a.get("type"), "approved": a.get("approved")}
            for a in cdata.get("validated_assets", [])
        ],
        "namespace_indexed_at": __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    filepath = os.path.join(INDEX_DIR, f"{cid}.json")
    with open(filepath, "w") as f:
        json.dump(namespace, f, indent=2)
    print(f"Indexed: {cid} → {filepath}")

# Write master index
index = {
    "total_clients": len(clients),
    "active_clients": len(db.get("index", {}).get("by_status", {}).get("active", [])),
    "clients": [
        {
            "client_id": cid,
            "name": c.get("client_name"),
            "status": c.get("status"),
            "assets": len(c.get("validated_assets", [])),
            "campaigns": len(c.get("campaigns", []))
        }
        for cid, c in sorted(clients.items())
    ],
    "generated_at": __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
}

with open(os.path.join(INDEX_DIR, "_index.json"), "w") as f:
    json.dump(index, f, indent=2)

print(f"\nMaster index written: {len(clients)} clients indexed.")
print(f"Index directory: {INDEX_DIR}")