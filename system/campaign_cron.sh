#!/usr/bin/env bash
# campaign_cron.sh - Daily Campaign Cycle Wrapper
# This script is intended to be called by a daily cron job.

LOG_FILE="/home/team/shared/logs/campaign_cycle.log"
SCRIPT_PATH="/home/team/shared/scripts/campaign_cycle.py"

echo "[$(date)] Starting daily campaign cycle..." >> "$LOG_FILE"
python3 "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1
echo "[$(date)] Campaign cycle finished." >> "$LOG_FILE"
