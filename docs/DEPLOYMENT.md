# Seyalla Phase 4 Deployment Guide

This guide is a startup-friendly deployment path for Seyalla v1.

## Recommended hosting stack (practical v1)

### Frontend host (React/Vite)
**Recommended:** Vercel
- Fast static hosting + global CDN
- Simple Git-based deploys
- Easy environment variable management

### Backend host (FastAPI)
**Recommended:** Render Web Service (or Railway as equivalent)
- Easy Python deployment from Git
- Managed HTTPS and environment variables
- Health checks + log streaming included

### Database host
**Recommended:** Supabase Postgres
- Managed PostgreSQL
- Built-in auth and row-level security options (if needed later)
- Easy connection management and backups

---

## Environment variables

## Backend (`app`)
- `SEYALLA_APP_NAME=Seyalla Backend API`
- `SEYALLA_APP_VERSION=1.0.0`
- `SEYALLA_ENVIRONMENT=production`
- `SEYALLA_DEBUG=false`
- `SEYALLA_DATABASE_URL=postgresql://<user>:<pass>@<host>:5432/<db>`

Suggested additional v1 vars:
- `SEYALLA_ALLOWED_ORIGINS=https://<frontend-domain>`
- `SEYALLA_API_KEY=<server-to-server-key-if-needed>`
- `SEYALLA_LOG_LEVEL=INFO`

## Frontend (`frontend`)
- `VITE_API_BASE_URL=https://<backend-domain>`

---

## Local setup steps

1. **Clone and install backend dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run backend**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Install and run frontend**
   ```bash
   cd frontend
   npm install
   VITE_API_BASE_URL=http://127.0.0.1:8000 npm run dev
   ```

4. **Open apps**
- Backend docs: `http://127.0.0.1:8000/docs`
- Frontend: usually `http://127.0.0.1:5173`

---

## Production deployment steps

### 1) Database (Supabase)
1. Create a Supabase project.
2. Apply schema from `app/db/schema.sql`.
3. Create DB user and connection string.
4. Add DB backups and retention policy.

### 2) Backend (Render)
1. Create new Web Service from repo.
2. Build command:
   ```bash
   pip install -r requirements.txt
   ```
3. Start command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. Add environment variables listed above.
5. Configure health check path: `/health`.
6. Restrict CORS to frontend domain.

### 3) Frontend (Vercel)
1. Import repo in Vercel.
2. Set root directory to `frontend`.
3. Build command:
   ```bash
   npm run build
   ```
4. Output directory: `dist`.
5. Add `VITE_API_BASE_URL` pointing to backend.
6. Deploy and verify API calls from UI.

### 4) Post-deploy checks
- Validate `/health` returns `ok`.
- Validate role-based flows for staff and admin.
- Confirm no cross-store data leakage.
- Test chat, summary, analytics, anomalies, and recommendations from frontend.

---

## Logging and monitoring basics (v1)

### Backend logging
- Use structured JSON logs if possible (`request_id`, `path`, `user_id`, `role`, `status_code`, latency).
- Never log raw secrets, tokens, or sensitive staff PII.
- Log AI endpoint usage counts and error rates.

### Metrics to track
- Request volume by endpoint (`/chat`, `/summary`, `/analytics`, `/anomalies`, `/recommendations`)
- p95 latency per endpoint
- 4xx and 5xx error rate
- DB query latency
- Anomaly volume trends (to detect alert noise)

### Basic monitoring setup
- Render/Railway built-in logs + alerts for service downtime.
- Uptime monitor (e.g., Better Stack/UptimeRobot) on `/health`.
- Sentry for backend exception tracing.

---

## Security considerations (role-based data + AI endpoints)

1. **Authentication first**
- Replace mock requester context with JWT/session auth in production.
- Never trust role/user identity from frontend payload alone.

2. **Server-side authorization**
- Enforce role checks on every endpoint (already structured in service layer).
- Keep store-level and staff-level scoping in backend only.

3. **CORS and origin control**
- Allow only trusted frontend origins.
- Disable wildcard origins in production.

4. **Rate limiting and abuse protection**
- Add per-user and per-IP throttles for `/chat` and analytics endpoints.
- Add payload size limits and request timeouts.

5. **Secrets management**
- Store DB URLs/API keys in platform secret managers.
- Rotate secrets regularly.

6. **Data protection**
- TLS everywhere (frontend, backend, DB).
- Encrypt sensitive fields at rest where applicable.
- Keep audit logs for access to manager/admin insights.

7. **AI endpoint safety**
- Validate and sanitize user prompts before use.
- Prevent prompt injection from accessing unauthorized data.
- Keep deterministic business logic (commission/rules) out of LLM generation path.

8. **Operational safety**
- Add dependency patching cadence.
- Add backup + restore drills for PostgreSQL.
- Document incident response for data exposure or auth bypass.
