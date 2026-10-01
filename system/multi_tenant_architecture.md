# Kaleiora Multi-Tenant Vector DB Architecture

**Version**: 2.0
**Date**: 2026-06-06
**Author**: Brand Custodian Agent

---

## 1. Architecture Overview

The Client Vector Database is designed as a **multi-tenant document store** where each tenant (client) operates in an isolated namespace with their own brand DNA, creative assets, and campaign cycles.

```
┌─────────────────────────────────────────────────────────┐
│                  CLIENT VECTOR DB                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  NovaTech    │  │  GreenLeaf   │  │  FinFlow     │  │
│  │  Solutions   │  │  Organics    │  │  Accounting  │  │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  │
│  │ Brand DNA    │  │ Brand DNA    │  │ Brand DNA    │  │
│  │ Tone/Voice   │  │ Tone/Voice   │  │ Tone/Voice   │  │
│  │ Visual ID    │  │ Visual ID    │  │ Visual ID    │  │
│  │ Assets[]     │  │ Assets[]     │  │ Assets[]     │  │
│  │ Campaigns[]  │  │ Campaigns[]  │  │ Campaigns[]  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │            SHARED VALIDATION LOG                  │   │
│  │  (client_id scoped; no cross-tenant leakage)     │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │         INDEX: by_status | by_agent | by_cycle   │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Namespace Isolation** — Each client's data is scoped under their `client_id` key. No cross-client data access without explicit authorization.
2. **Unlimited Horizontal Scaling** — Adding new clients is an O(1) operation. Simply append to the `clients` dictionary.
3. **Parallel Campaign Support** — Each client maintains an independent array of campaign cycles.
4. **Single Source of Truth** — All brand DNA, assets, and validation history are stored in one file for atomic consistency.

---

## 2. Schema Design

### Client Record Structure

```json
{
  "clients": {
    "{client_id}": {
      "client_name": "string",
      "status": "intake | active | archived",
      "created_at": "ISO timestamp",
      "updated_at": "ISO timestamp",
      
      "brand_guidelines": "{...}",       // Brand DNA namespace
      "tone_of_voice": "{...}",          // Voice & tone namespace
      "visual_identity": "{...}",        // Visual identity namespace
      
      "campaigns": [                      // PARALLEL CAMPAIGN CYCLES
        {
          "campaign_id": "uuid",
          "name": "string",
          "status": "planning | active | paused | completed",
          "start_date": "ISO timestamp",
          "end_date": "ISO timestamp",
          "channels": ["social", "email", "ads", "landing"],
          "objectives": ["ROAS", "brand_awareness", "lead_gen"],
          "budget": "number (USD)",
          "current_roas": "number",
          "assets": ["asset_id", ...],   // References to validated assets
          "kpis": {
            "impressions": "number",
            "clicks": "number",
            "conversions": "number",
            "spend": "number"
          }
        }
      ],
      
      "validated_assets": [{...}],       // Quality-gate passed assets
      
      "intake_data": "{...}",            // Original intake form data
      
      "namespace_metadata": {             // Auto-scaling metadata
        "total_assets_created": "number",
        "total_validations_run": "number",
        "last_campaign_id": "uuid",
        "storage_estimate_bytes": "number"
      }
    }
  }
}
```

### Namespace Isolation Rules

| Operation | Isolation Level | Enforcement |
|-----------|----------------|-------------|
| Brand Guideline Reads | Per-client | Keyed by `clients[client_id].brand_guidelines` |
| Asset Validation | Per-client | Quality Gate reads only the target client's brand DNA |
| Campaign Management | Per-client | Campaigns array is scoped under each client |
| Audit Trail | Scoped by `client_id` | Validation log entries tagged with `client_id` |
| Search | Full DB or scoped | `search` command accepts optional `client_id` flag |

---

## 3. Campaign Cycle Architecture

Each client can run **N parallel campaign cycles** simultaneously. Campaigns are:

- **Fully isolated** — No cross-client campaign data
- **Asset-linked** — Each campaign references validated asset IDs
- **KPI-tracked** — ROAS, impressions, clicks, conversions tracked per campaign
- **Lifecycle-managed** — Status transitions: planning → active → paused → completed

### Campaign Lifecycle

```
PLANNING → ACTIVE → COMPLETED
               ↓
            PAUSED → ACTIVE
```

---

## 4. CLI Commands for Multi-Tenant Operations

### New Commands

| Command | Description |
|---------|-------------|
| `campaign create <client_id> <name>` | Create a new campaign for a client |
| `campaign list <client_id>` | List all campaigns for a client |
| `campaign activate <client_id> <campaign_id>` | Start a campaign |
| `campaign complete <client_id> <campaign_id>` | Complete a campaign |
| `validate-all <dir>` | Batch validate all asset files in a directory against their respective clients |
| `namespace check <client_id>` | Verify data isolation for a client (no leakage) |
| `search <term> [client_id]` | Scope search to specific client (optional) |

### Updated Commands

- `validate` — Now also links approved assets to an optional campaign
- `list` — Shows campaign count per client
- `stats` — Shows campaign statistics

---

## 5. Auto-Scaling Design

### Scaling Characteristics

| Scale Level | Clients | DB File Size (est.) | CLI Performance |
|-------------|---------|---------------------|-----------------|
| Starter | 1-10 | < 5 MB | Instant |
| Growth | 10-100 | < 50 MB | < 1 sec |
| Agency | 100-1,000 | < 500 MB | < 2 sec |
| Enterprise | 1,000+ | Shard recommended | Partition needed |

### Sharding Strategy (for 1,000+ clients)

When the DB exceeds 1,000 clients or 500 MB:

```json
{
  "shards": {
    "shard_001": "client_vector_db_001.json",  // clients A-H
    "shard_002": "client_vector_db_002.json",  // clients I-P
    "shard_003": "client_vector_db_003.json"   // clients Q-Z
  },
  "shard_index": {
    "client-a": "shard_001",
    "client-b": "shard_001",
    ...
    "client-novatech-solutions-demo": "shard_002"
  }
}
```

### Memory Optimization

- **Lazy loading**: CLI reads only index first, loads client data on demand
- **Background archival**: Archived clients stored in separate `client_vector_db_archive.json`
- **Validation log rotation**: Logs older than 90 days moved to archive

---

## 6. Data Flow: End-to-End Multi-Tenant

```
1. CLIENT INTAKE
   Dashboard Form → Brand Custodian → Vector DB (new namespace)
                                         ↓
2. CREATIVE GENERATION
   Creative Agent → Retrieves Brand DNA from Vector DB
                      → Generates asset aligned to brand
                                         ↓
3. QUALITY GATE (Per-Client Namespace)
   Asset → Brand Custodian → Validates against client's:
     - brand_guidelines
     - tone_of_voice.do_say / dont_say
     - tone_of_voice.vocabulary.preferred_terms / avoid_terms
                              ↓
                     PASSED  ───→  Added to validated_assets[]
                     REJECTED ──→  Logged, creator notified
                                         ↓
4. CAMPAIGN LINKING
   Approved Asset → Linked to campaign cycle
                     → Ready for Final Delivery
                                         ↓
5. FINAL DELIVERY
   Brand Custodian pushes → Dashboard "Final Delivery" section
```

---

## 7. Tenant Demonstration

Currently indexed tenants:

| # | Client ID | Name | Industry | Status | Assets | Campaigns |
|---|-----------|------|----------|--------|--------|-----------|
| 1 | `client-novatech-solutions-demo` | NovaTech Solutions | AI / SaaS | active | 18 | 0 |
| 2 | `client-greenleaf-organics-demo` | GreenLeaf Organics | Organic Food | active | 0 | 0 |
| 3 | `client-finflow-accounting-demo` | FinFlow Accounting | FinTech | active | 0 | 0 |

Each tenant has:
- ✅ Isolated brand guidelines namespace
- ✅ Independent tone of voice with do_say/dont_say lists
- ✅ Separate visual identity (colors, typography, imagery)
- ✅ Own validated assets array (zero cross-contamination)
- ✅ Ready for parallel campaign cycles

---

## 8. Security & Isolation Guarantees

1. **No cross-tenant read**: The `get` command only returns data for the requested `client_id`
2. **No cross-tenant write**: The `validate` engine only reads the target client's brand DNA
3. **Scoped validation log**: Every log entry is tagged with `client_id` for audit traceability
4. **Namespace metadata**: Each client tracks its own usage statistics independently
5. **Index integrity**: The `by_status` index maintains correct client membership

---

## 9. Upgrade Path: v1.0 → v2.0

| Feature | v1.0 (Current) | v2.0 (Multi-Tenant) |
|---------|----------------|---------------------|
| Max Clients | Unlimited in theory | Tested with 3+ |
| Campaign Tracking | ❌ Not available | ✅ campaigns[] per client |
| Batch Operations | ❌ Single-client only | ✅ validate-all, batch |
| Namespace Isolation | ✅ Basic (per key) | ✅ Enhanced (scoped operations) |
| CLI Commands | 12 | 18+ |
| Architecture Doc | ❌ None | ✅ This document |
| Sample Clients | 1 | 3 (diverse industries) |