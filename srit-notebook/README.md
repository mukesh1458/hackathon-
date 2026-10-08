# Supabase High-Availability Demo (Aigerdata / Ristara)

This repository contains the architecture, scripts, and CI/CD pipelines to prove that self-hosted Supabase can replace Firebase and comfortably achieve a 99.9% uptime SLA for Ristara.

## Architecture

We use a dual-stack configuration powered by Docker Compose:
- **`dev/` Stack:** Used for active development and staging. Runs on ports 8000+ and 5432.
- **`prod/` Stack:** Used for live traffic. Runs on ports 8080+ and 5433.

Both stacks are entirely isolated. They have distinct `COMPOSE_PROJECT_NAME` values, separated `.env` files with securely generated cryptographic keys (no default Supabase keys), and completely independent Postgres volumes.

### CI/CD Deployment
A local GitHub Actions workflow (`.github/workflows/deploy.yml`) handles continuous integration and deployment. 
- Pushing to the `dev` branch triggers a deployment to the local `dev` Docker stack.
- Pushing to the `main` branch triggers tests and a deployment to the `prod` Docker stack, including an automated rollback mechanism if the API container fails to report as healthy.

---

## Achieving 99.9% Uptime

A 99.9% uptime SLA allows for exactly **43.83 minutes of downtime per month**. We achieve this through the following layers of resilience:

1. **Docker `unless-stopped` Policies:** Every container in the Supabase stack is configured with native restart policies. If the REST API or GoTrue crashes due to an out-of-memory error, Docker instantly restarts it (typically taking < 5 seconds, resulting in zero noticeable downtime if load balanced).
2. **Native Healthchecks:** Critical services (Postgres, Kong, PostgREST, Auth) have Docker healthchecks. If an API becomes unresponsive but doesn't crash, the healthcheck fails, and the container is rebooted.
3. **Graceful Maintenance Windows:** The `maintenance_restart.sh` script handles updates and restarts gracefully.
4. **Environment Isolation:** (See `COMPARISON.md`). By strictly separating `dev` and `prod`, we eliminate the "noisy neighbor" problem where a bad dev query crashes the production database.

---

## Demo Script (Step-by-Step for Aigerdata Team)

Follow these steps to demonstrate the system to the client:

### Step 1: Start the Stacks
1. Navigate to the `dev` directory and run: `docker compose up -d`
2. Navigate to the `prod` directory and run: `docker compose up -d`
3. Show the client the isolated ports running via `docker ps`.

### Step 2: Demonstrate Uptime Monitoring
1. Run `./health_check.sh &` in the background. Explain that this represents an external uptime monitor (like BetterUptime) pinging the API every 30 seconds.
2. Let it run for a minute to generate some entries in `health.log`.
3. Run `python uptime_calculator.py` to show the perfect 100% initial uptime.

### Step 3: Simulate a Catastrophic Failure
1. Run `./simulate_failure.sh`. This script will hunt down the Production REST API container and abruptly `kill` it.
2. Watch the terminal output. Docker's event stream will show the container being automatically recreated and started within seconds.
3. Tail the `health.log`. You may see a single `DOWN` entry, immediately followed by `UP` entries again. 
4. Run `python uptime_calculator.py` again. The uptime will dip to ~99.9X%, proving the system's resilience and auto-recovery capabilities well within the 43-minute monthly budget.

### Step 4: CI/CD & Migrations
1. Show the client `.github/workflows/deploy.yml`. 
2. Highlight the `Apply Database Migrations` step utilizing the `supabase/migrations` folder, proving that schema changes are tracked in version control and applied safely, eliminating manual database edits that often cause outages.
