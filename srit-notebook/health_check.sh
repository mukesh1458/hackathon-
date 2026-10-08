#!/bin/bash
# health_check.sh
# Pings the Supabase REST API every 30s and logs UP/DOWN with a timestamp to health.log.

API_URL="http://localhost:8080/rest/v1/"
LOG_FILE="health.log"

while true; do
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Ping the API (using curl with a 5s timeout)
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 $API_URL)
    
    if [ "$HTTP_STATUS" -eq 200 ] || [ "$HTTP_STATUS" -eq 401 ] || [ "$HTTP_STATUS" -eq 404 ]; then
        # 401 or 404 from PostgREST means the API is up but we didn't provide auth or queried root. That's UP.
        echo "[$TIMESTAMP] UP" >> $LOG_FILE
    else
        echo "[$TIMESTAMP] DOWN (Status: $HTTP_STATUS)" >> $LOG_FILE
    fi
    
    sleep 30
done
