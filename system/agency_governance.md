# Kaleiora Agency Governance & Vision

## 1. Agency Vision
Kaleiora Agentic Marketing is a next-generation marketing agency powered by an autonomous, self-correcting AI swarm. Our mission is to deliver world-class marketing ROI through 100% operational transparency and rigorous quality validation. 

**Core Tenets:**
- **Agentic Autonomy:** Agents own their roles and outcomes.
- **Real-Time Transparency:** All progress is visible on the live Command Center.
- **No Output without Validation:** All creative must pass the Vector DB and CI critique.
- **Aggressive Feedback:** Continuous self-reflection and performance tuning.

## 2. Red-Line Auto-Trigger Protocol
This protocol ensures autonomous crisis detection and near-zero latency response activation.

### Detection Mechanism
- **Monitoring Loop:** The Continuous Improvement (CI) Agent is mandated to automatically monitor the Brand Health Score (BHS) immediately following every calculation within the `sync_bhs.py` pipeline.
- **Critical Threshold:** A calculated BHS below **50** triggers an immediate Red-Line event.
- **Bypass Logic:** This automated trigger operates as a hard-coded safety logic within the synchronization scripts, bypassing manual approval or human intervention.

### Alert Format & Communication
- **Alert Channel 1 (Kanban):** An automated high-priority task is created in the `tasks` table assigned to the Marketing Manager.
- **Alert Channel 2 (Direct):** A high-priority `send_message` is dispatched to the Crisis Commander.
- **Standard Alert Content:** `[RED-LINE ALERT] Client: <ID> | Current BHS: <Score> | Trigger: <Metric> | Action: RETRACT/REVERT/FIX`.

### Escalation Timeline
- **T+0 (Immediate):** Auto-detection triggers "RED-LINE EMERGENCY" dashboard status and manager alerts.
- **T+5m:** Marketing Manager (Crisis Commander) acknowledges and activates the swarm.
- **T+15m:** CI and Dev Agents provide a data-driven autopsy report.
- **T+30m:** Recovery asset (e.g., ad revert, code patch) is deployed and verified.
- **T+60m:** Mandatory debrief is documented in `/home/team/shared/logs/`; dashboard status is reset to "OPTIMIZED".

### System Integration
The `sync_bhs.py` script acts as the primary integration point. Every 60 seconds (or upon manual trigger), the script:
1. Retrieves raw metrics from `brand_health_score.json`.
2. Executes the CI Agent's calculation logic.
3. Updates the live `command_center.html` via `dashboard_data.json`.
4. **Evaluates Red-Line Status:** If criteria are met, it executes the Alert Format protocols.

## 3. Red-Line Recovery Protocol (Crisis Management)
The Marketing Manager (Crisis Commander) has sole authority to trigger and resolve Red-Line events manually if necessary.

### Protocol Steps
1. **Status Change:** Marketing Manager sets Dashboard status to "RED-LINE EMERGENCY".
2. **Autopsy:** CI Agent and Analytics provide data-driven post-mortems to the Manager.
3. **Patch:** Marketing Manager orders specific updates, prompt tuning, or process changes from the relevant agents.
4. **Resolution:** Manager verifies the fix and uploads a "Recovery Asset" to the dashboard.
5. **Debrief:** Status reset to "OPTIMIZED." A brief summary of the recovery is archived in the agency logs.

## 4. Communication Escalation Paths
- **Dashboard Sync:** The primary communication channel is the live dashboard. Agents must push status updates to `dashboard_data.json` via the standard update scripts.
- **Inter-Agent Coordination:** Agents use `send_message` for direct collaboration or when blocked.
- **Lead Review:** Final deliverables and major architectural changes require Team Lead approval via the Kanban board.
- **Emergency Escalation:** Any agent discovering a critical failure (e.g., brand violation, ROI collapse) must immediately message the Marketing Manager to evaluate for Red-Line status.

## 4. Daily Performance Digest Template (08:00 EST)
The Marketing Manager provides a visual digest on the dashboard every morning.

- **Status Overview:** Total projects active, completed, and in Red-Line status.
- **Agency KPIs:**
    - Composite Brand Health Score (Target: >90)
    - Average Performance ROI (ROAS/CAC)
    - Recovery Time (MTTR for Red-Lines)
- **Top Campaign Highlights:** Wins and optimizations from the last 24 hours.
- **Focus Areas:** Specific agents or tasks requiring attention today.

## 5. Monitoring & Sync Cadence
- **Instant:** Status updates and dashboard sync (Developer Agent).
- **Hourly:** Marketing Manager check-in on Brand Health scores and critical project statuses.
- **Daily:** Performance Digest issued at 08:00 EST.
- **Weekly:** Swarm Reflection — reviewing CI Agent reports to identify systemic improvements.
