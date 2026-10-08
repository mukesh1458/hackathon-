import yaml
import sys

def modify_compose(path):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
        
    for service_name, service in data.get('services', {}).items():
        # Enforce restart policy
        service['restart'] = 'unless-stopped'
        
        # Add basic healthcheck if missing
        if 'healthcheck' not in service:
            if service_name == 'db':
                service['healthcheck'] = {
                    'test': ['CMD', 'pg_isready', '-U', 'postgres', '-h', '127.0.0.1', '-p', '5432'],
                    'interval': '5s',
                    'timeout': '5s',
                    'retries': 5
                }
            elif service_name == 'rest':
                service['healthcheck'] = {
                    'test': ['CMD', 'wget', '--no-verbose', '--tries=1', '--spider', 'http://127.0.0.1:3000/'],
                    'interval': '10s',
                    'timeout': '5s',
                    'retries': 3
                }
            elif service_name == 'auth':
                service['healthcheck'] = {
                    'test': ['CMD', 'wget', '--no-verbose', '--tries=1', '--spider', 'http://127.0.0.1:9999/health'],
                    'interval': '10s',
                    'timeout': '5s',
                    'retries': 3
                }
            elif service_name == 'api-gw':
                service['healthcheck'] = {
                    'test': ['CMD', 'kong', 'health'],
                    'interval': '10s',
                    'timeout': '5s',
                    'retries': 3
                }
            else:
                # Generic fallback if no healthcheck
                service['healthcheck'] = {
                    'test': ['CMD', 'echo', 'ok'],
                    'interval': '30s',
                    'timeout': '10s',
                    'retries': 3
                }
                
    with open(path, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

modify_compose('dev/docker-compose.yml')
modify_compose('prod/docker-compose.yml')
print("Docker compose files updated with healthchecks and restart policies.")
