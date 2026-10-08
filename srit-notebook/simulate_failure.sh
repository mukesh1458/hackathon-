#!/bin/bash
# simulate_failure.sh
# Intentionally kills a critical Supabase container to demonstrate auto-recovery.

echo "Identifying a running Supabase container..."
# Using rest (PostgREST) as our target
CONTAINER_NAME=$(docker ps --format "{{.Names}}" | grep prod-supabase-rest)

if [ -z "$CONTAINER_NAME" ]; then
    echo "No prod-supabase-rest container found. Are you running 'docker compose up' in prod?"
    # Fallback to dev for demo purposes if prod is down
    CONTAINER_NAME=$(docker ps --format "{{.Names}}" | grep dev-supabase-rest)
fi

if [ -z "$CONTAINER_NAME" ]; then
    echo "Error: No Supabase REST container found to kill."
    exit 1
fi

echo "Found container: $CONTAINER_NAME"
echo "Simulating sudden failure (kill)..."
docker kill $CONTAINER_NAME

echo "Container killed. Watch the health.log and docker ps to observe Docker's unless-stopped policy recovering the service."
echo "Tailing docker events for container start..."
docker events --filter event=start --filter container=$CONTAINER_NAME &
EVENTS_PID=$!

sleep 10
kill $EVENTS_PID

echo "Failure simulation complete. Check uptime_calculator.py to see the impact on uptime."
