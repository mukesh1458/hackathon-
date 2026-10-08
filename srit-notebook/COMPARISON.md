# Supabase Architecture Analysis: Isolated Projects vs. Shared Database

When deciding how to host multiple Supabase projects (e.g. dev, staging, prod, or multiple clients) using self-hosted infrastructure, there are two primary approaches:
1. **Isolated Projects (e.g., using a PaaS like Coolify or individual Docker Swarms)**
2. **Shared Database / Shared Server (multi-tenant on one large Postgres instance/server)**

This document analyzes both approaches for the Aigerdata/Ristara requirements.

---

## 1. Blast Radius and Uptime Risk (The 99.9% Goal)
**Isolated Projects:**
- **Advantage:** Total isolation. If the `dev` database crashes due to a massive unindexed query, or if a specific Docker node runs out of memory, `prod` is completely unaffected. 
- **Uptime:** Essential for hitting 99.9% uptime (max 43.8 minutes downtime per month). A kernel panic on the dev server won't touch prod.

**Shared Server:**
- **Risk:** High. A noisy neighbor problem is inevitable. A developer running a heavy data migration in `dev` will consume CPU, causing latency spikes or timeouts in `prod` API requests. If the shared Postgres instance crashes, all environments go down simultaneously.

## 2. Resource Utilization
**Isolated Projects:**
- **Heavier Footprint:** Each Supabase stack runs its own GoTrue (Auth), PostgREST (API), Realtime, Storage, and Postgres instances. This means ~10-14 containers per environment. You need more base RAM (typically a minimum of 2GB-4GB per stack just for idle overhead).

**Shared Server:**
- **Lighter Footprint:** You only run one massive Postgres instance and one set of API containers, using schema-based multi-tenancy or logical databases. Much more memory-efficient at scale.

## 3. Cost
**Isolated Projects:**
- **Higher initial cost:** You must provision separate servers or larger clustered droplets to handle the baseline overhead of multiple container stacks.

**Shared Server:**
- **Lower cost:** Better bin-packing of resources. You pay for one large, optimized server rather than multiple smaller ones.

## 4. Maintenance and Upgrades
**Isolated Projects:**
- **Safer:** You can upgrade the Supabase version in `dev`, verify it for a week, and then roll the upgrade to `prod`. 
- **Rollbacks:** Easier to roll back a single project if an upgrade fails.

**Shared Server:**
- **Risky:** Upgrading the shared Postgres instance or API gateway affects all environments instantly.

---

## Conclusion & Recommendation

To achieve a true **99.9% SLA for Ristara**, you cannot compromise on the blast radius. 

**Recommendation:**
- **Production (`prod`):** MUST be isolated on its own server/droplet or dedicated Coolify project.
- **Development/Staging (`dev`):** Can be shared on a cheaper, combined server (or run locally via the CI/CD self-hosted runner) to save costs.

Using a tool like **Coolify** makes the isolated approach almost as easy to manage as a shared server, giving you PaaS-like deployments while maintaining strict physical and network boundaries between environments.
