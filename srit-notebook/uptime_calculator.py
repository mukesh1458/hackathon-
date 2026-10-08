import sys
import os
from datetime import datetime, timedelta

def calculate_uptime(log_file):
    if not os.path.exists(log_file):
        print("Log file not found.")
        return

    now = datetime.utcnow()
    day_ago = now - timedelta(days=1)
    
    total_checks = 0
    up_checks = 0
    
    with open(log_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                # Format: [2026-10-08T08:34:07Z] UP
                timestamp_str = line.split('] ')[0].strip('[')
                status = line.split('] ')[1].split(' ')[0]
                
                log_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
                
                if log_time >= day_ago:
                    total_checks += 1
                    if status == "UP":
                        up_checks += 1
            except Exception as e:
                pass
                
    if total_checks == 0:
        print("No logs in the last 24 hours.")
    else:
        uptime_pct = (up_checks / total_checks) * 100
        print(f"Total checks (24h): {total_checks}")
        print(f"Successful checks:  {up_checks}")
        print(f"Uptime:             {uptime_pct:.3f}%")

if __name__ == "__main__":
    calculate_uptime('health.log')
