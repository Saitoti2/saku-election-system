## Backend Overview

This project currently contains two Django codebases. Only one is active in local demos and deployments. Use this guide as the source of truth for backend-related work.

### Active backend (`saku-strategy/backend`)
- Django project module: `core`
- Entry points:
  - `python manage.py runserver` (local development)
  - `app.py` → `core.settings` (container/serverless deployments)
- Dependencies: `saku-strategy/backend/requirements.txt`
- App modules: business logic for registrations lives in `elections/`
- Static assets are collected into `staticfiles/`

### Legacy scaffold (`saku_election`)
- Earlier prototype of the API kept for reference.
- Not referenced by any tooling (`start.sh`, Dockerfile, Railway, Render, etc.).
- Safe to ignore for day-to-day work; don’t install requirements from this folder.

### Working with the backend
- Activate the project virtualenv (`source venv/bin/activate`) or run `./start.sh`.
- Run management commands from `saku-strategy/backend` (e.g. `python manage.py migrate`).
- Configuration is in `saku-strategy/backend/core/settings.py`. Change environment variables via `.env` (copy from `env_template.txt`).
- Tests live in `saku-strategy/backend/elections/tests.py` and can be executed with `pytest` or `python manage.py test`.

### Useful commands
```bash
# Start full stack (recommended)
./start.sh

# Backend only
cd saku-strategy/backend
source ../../venv/bin/activate
python manage.py runserver 0.0.0.0:8001

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

> Need to locate the active backend quickly? Remember: **if it’s not inside `saku-strategy/backend`, it’s not the live API.**

