# Kaleiora Brand Health Score (BHS) Methodology

## Overview
The Brand Health Score (BHS) is a proprietary composite metric designed to provide a real-time snapshot of account health, performance, and alignment. It is the primary KPI rendered on the Kaleiora Command Center dashboard.

## The Formula
The BHS is calculated as a weighted average of five core pillars:

**BHS = (0.25 × ROAS) + (0.20 × CAC) + (0.25 × Alignment) + (0.15 × Velocity) + (0.15 × Sentiment)**

### 1. ROAS Score (25%)
*   **Definition:** Efficiency of advertising spend.
*   **Calculation:** `(Actual ROAS / Target ROAS) * 100`
*   **Cap:** 120 points.

### 2. CAC Efficiency Score (20%)
*   **Definition:** Customer Acquisition Cost relative to targets.
*   **Calculation:** `(Target CAC / Actual CAC) * 100`
*   **Cap:** 120 points.

### 3. Brand Alignment Score (25%)
*   **Definition:** Qualitative and quantitative measure of how well creative outputs match the Client Vector Database.
*   **Source:** Validated by the Brand Custodian and critiqued by the CI Agent.
*   **Scale:** 0 - 100.

### 4. Operational Velocity (15%)
*   **Definition:** Timeliness of deliverables and task completion rates.
*   **Calculation:** `(Tasks Completed On-Time / Total Tasks Due) * 100`
*   **Scale:** 0 - 100.

### 5. Client Sentiment (15%)
*   **Definition:** Signal-based satisfaction (from direct feedback, meeting sentiment, or survey results).
*   **Source:** Inputted by the Marketing Manager.
*   **Scale:** 0 - 100.

## Status Indicators
The BHS translates into a visual status on the dashboard:

| Score Range | Status | Color | Action Required |
| :--- | :--- | :--- | :--- |
| **75 - 100+** | **OPTIMIZED** | Green | Maintain momentum; seek incremental gains. |
| **50 - 74** | **STABLE** | Yellow | Monitor closely; identify sub-par pillars for adjustment. |
| **0 - 49** | **RED-LINE** | Red | **CRISIS PROTOCOL:** Trigger Red-Line Recovery immediately. |

## Continuous Improvement Loop
The CI Agent (Continuous Improvement Agent) reviews these scores daily. Any pillar dropping below 60 triggers an automatic internal critique and recommendation for the relevant agent role.
