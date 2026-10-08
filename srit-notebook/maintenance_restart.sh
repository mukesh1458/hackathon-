#!/bin/bash
# maintenance_restart.sh
# Safely restarts the Supabase Docker stack for daily maintenance.
# 
# To install this cron entry for a 3 AM daily restart, run:
# (crontab -l 2>/dev/null; echo "0 3 * * * /path/to/maintenance_restart.sh") | crontab -

echo "Starting daily maintenance restart..."
cd prod || exit 1

# Bring down services gracefully
docker compose down

# Bring services back up
docker compose up -d

echo "Maintenance complete."
