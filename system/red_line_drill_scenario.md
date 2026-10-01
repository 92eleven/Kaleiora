# Red-Line Crisis Drill Scenario: "Brand DNA Breach"

## 1. Scenario Overview
This drill simulates a critical process failure: a creative asset that failed brand validation is accidentally pushed live for our client "Apex Growth Lab," causing immediate brand reputation risk.

## 2. The Trigger (T-0:00)
- **Event:** A high-spend video ad containing unapproved "aggressive pressure tactics" and incorrect logo usage is deployed to Meta Ads.
- **Detection:** The Brand Custodian discovers the breach during a routine Vector DB sync check and realizes the asset in the "Final Delivery" folder was not the validated version.
- **Alert Message:** "RED-LINE ALERT: Brand DNA Breach. Unvalidated asset 'APEX_V3_AGGRESSIVE' is LIVE. Immediate retraction required."

## 3. Recovery Protocol Execution (Expected Steps)

### Phase 1: Activation (Goal: <5 mins)
- **Marketing Manager (Crisis Commander):** Verifies the breach. 
- **Action:** Execute `python3 /home/team/shared/update_dashboard.py global_status "RED-LINE EMERGENCY"`.
- **Action:** Notify the swarm via `send_message`: "RED-LINE EMERGENCY: Brand DNA Breach for Apex. Protocol Omega. All hands on deck for asset retraction and replacement."

### Phase 2: Autopsy & Identification (Goal: <10 mins)
- **CI Agent:** Assesses early sentiment/performance. Flags a spike in "Negative Feedback" on the ad.
- **Brand Custodian:** Identifies exactly how the unvalidated asset bypassed the Quality Gate (e.g., manual override or sync error).
- **Finding:** The autopsy reveals a "Shadow Update" was pushed without the `VALIDATED` tag in the Vector DB.

### Phase 3: Patch & Resolution (Goal: <20 mins)
- **Dev Agent:** Immediately pauses the ad campaign.
- **Brand Custodian:** Provides the correct, validated asset from the Vector DB.
- **Dev Agent:** Replaces the faulty asset with the "Recovery Asset" (Apex_V2_Validated) and restarts the campaign.
- **Action:** Marketing Manager verifies the live state and updates the dashboard with the "Recovery Asset" status.

### Phase 4: Normalization (Goal: <30 mins)
- **CI Agent:** Confirms brand health indicators are stabilizing.
- **Marketing Manager:** Resets status via `python3 /home/team/shared/update_dashboard.py global_status "OPTIMIZED"`.
- **Action:** Document the debrief and process fix (e.g., locking the Final Delivery folder to agents without Custodian approval) in `/home/team/shared/logs/red_line_autopsy_apex_002.md`.

## 4. Success Criteria
1. **Retraction Speed:** Faulty asset paused within 10 minutes of alert.
2. **Protocol Adherence:** Dashboard correctly reflects "RED-LINE EMERGENCY" status.
3. **Tool Proficiency:** Effective use of `update_dashboard.py` and `send_message`.
4. **Process Fix:** A specific recommendation to prevent "Shadow Updates" is included in the debrief.
