# Seyalla Backend (FastAPI)

Backend API for Seyalla (Seyal app AI layer), built as a practical modular FastAPI service.

## Project structure

```text
app/
  main.py                  # FastAPI app factory + router mount
  core/config.py           # Environment/config settings
  api/routes.py            # HTTP endpoints
  models/schemas.py        # Request/response contracts
  data/seed.py             # Seed/sample data (in-memory v1)
  services/
    container.py           # Service wiring
    intent_router.py
    analytics_service.py
    summary_service.py
    recommendation_service.py
    anomaly_detection.py   # Reusable anomaly logic
    anomaly_service.py
    role_guard.py          # Role-based access checks
    chat_service.py
  db/schema.sql            # PostgreSQL/Supabase-friendly schema
```

## Endpoints
- `GET /health`
- `POST /chat`
- `POST /summary`
- `POST /analytics`
- `POST /anomalies`
- `POST /recommendations`

## Local run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start API:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Open docs:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## Notes
- Current implementation is seed-data based for quick iteration.
- SQL schema in `app/db/schema.sql` is ready for migration to Supabase/PostgreSQL.

## Frontend (Phase 3)

```bash
cd frontend
npm install
npm run dev
```

Set API base URL if needed:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

## Deployment (Phase 4)

See practical deployment playbook: `docs/DEPLOYMENT.md`.
