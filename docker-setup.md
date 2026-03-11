# Docker Deployment Guide

## Prerequisites
- Docker and Docker Compose installed on your system.

## Steps

1. **Build the Docker images**:
   ```
   docker compose build
   ```

2. **Start the services in detached mode**:
   ```
   docker compose up -d
   ```

3. **Monitor logs** (especially app for initialization):
   ```
   docker compose logs -f app
   ```
   The app will automatically:
   - Connect to the PostgreSQL database (`db` service).
   - Create database if needed.
   - Initialize tables and seed initial data via [`main.py`](main.py).

4. **Access the application**:
   - API: http://localhost:5000
   - Logs show when ready: "All services started successfully."

5. **Optional: Run migrations manually** (if Alembic revisions added later):
   ```
   docker compose exec app python migrate.py
   ```

6. **Useful commands**:
   - View all logs: `docker compose logs -f`
   - Stop services: `docker compose down`
   - Reset database (remove volumes): `docker compose down -v`
   - Rebuild: `docker compose up --build -d`

## Notes
- `.env` file is used for configuration (DB_* vars, SECRET_KEY).
- `DB_HOST` is overridden to `db` (Postgres service name).
- No development volume mount (logs writen internally to container /app/application.log).
- View container logs with `docker compose logs`.
- Postgres data persists in `postgres_data` volume.
- Healthcheck ensures app starts after DB is ready.
- Port 5000 (Flask), 5432 (Postgres, optional external).