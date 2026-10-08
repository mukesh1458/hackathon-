import os
import secrets
import string
import jwt
import time

def generate_secret(length=32):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(length))

def generate_jwt_secret():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(40))

def update_env(source_path, target_path, is_prod):
    with open(source_path, 'r') as f:
        content = f.read()
    
    jwt_secret = generate_jwt_secret()
    postgres_password = generate_secret()
    
    # Generate valid JWTs
    # Anon Key Payload
    anon_payload = {
        "role": "anon",
        "iss": "supabase",
        "iat": int(time.time()),
        "exp": int(time.time()) + 315360000 # 10 years
    }
    # Service Role Key Payload
    service_role_payload = {
        "role": "service_role",
        "iss": "supabase",
        "iat": int(time.time()),
        "exp": int(time.time()) + 315360000
    }
    
    anon_key = jwt.encode(anon_payload, jwt_secret, algorithm="HS256")
    service_role_key = jwt.encode(service_role_payload, jwt_secret, algorithm="HS256")

    site_url = 'http://localhost:8080' if is_prod else 'http://localhost:8000'
    project_id = 'prod-supabase' if is_prod else 'dev-supabase'
    
    api_port = '8080' if is_prod else '8000'
    api_https_port = '8443' if is_prod else '8440'
    studio_port = '8082' if is_prod else '8002'
    db_port = '5433' if is_prod else '5432'
    pooler_port = '6544' if is_prod else '6543'
    pooler_tenant_port = '6545' if is_prod else '6546'
    pgmeta_port = '8083' if is_prod else '8003'
    gotrue_port = '8084' if is_prod else '8004'

    new_lines = []
    for line in content.split('\n'):
        if line.startswith('POSTGRES_PASSWORD='):
            line = f'POSTGRES_PASSWORD={postgres_password}'
        elif line.startswith('JWT_SECRET='):
            line = f'JWT_SECRET={jwt_secret}'
        elif line.startswith('ANON_KEY='):
            line = f'ANON_KEY={anon_key}'
        elif line.startswith('SERVICE_ROLE_KEY='):
            line = f'SERVICE_ROLE_KEY={service_role_key}'
        elif line.startswith('SITE_URL='):
            line = f'SITE_URL={site_url}'
        elif line.startswith('API_EXTERNAL_URL='):
            line = f'API_EXTERNAL_URL={site_url}'
        elif line.startswith('SUPABASE_PUBLIC_URL='):
            line = f'SUPABASE_PUBLIC_URL={site_url}'
        elif line.startswith('STUDIO_PORT='):
            line = f'STUDIO_PORT={studio_port}'
        elif line.startswith('KONG_HTTP_PORT='):
            line = f'KONG_HTTP_PORT={api_port}'
        elif line.startswith('KONG_HTTPS_PORT='):
            line = f'KONG_HTTPS_PORT={api_https_port}'
        elif line.startswith('POSTGRES_PORT='):
            line = f'POSTGRES_PORT={db_port}'
        elif line.startswith('POOLER_PORT='):
            line = f'POOLER_PORT={pooler_port}'
        elif line.startswith('POOLER_TENANT_PORT='):
            line = f'POOLER_TENANT_PORT={pooler_tenant_port}'
        elif line.startswith('COMPOSE_PROJECT_NAME='):
            line = f'COMPOSE_PROJECT_NAME={project_id}'
        # Just in case other conflicting ports exist:
        elif line.startswith('PGMETA_PORT='):
            line = f'PGMETA_PORT={pgmeta_port}'
        elif line.startswith('GOTRUE_PORT='):
            line = f'GOTRUE_PORT={gotrue_port}'
            
        new_lines.append(line)
        
    if not any(l.startswith('COMPOSE_PROJECT_NAME=') for l in new_lines):
        new_lines.append(f'COMPOSE_PROJECT_NAME={project_id}')
        
    with open(target_path, 'w') as f:
        f.write('\n'.join(new_lines))

update_env('dev/.env.example', 'dev/.env', is_prod=False)
update_env('prod/.env.example', 'prod/.env', is_prod=True)
print("Environment files generated with valid JWT secrets and isolated ports.")
