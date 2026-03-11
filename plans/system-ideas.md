# System Enhancement Ideas

## Core Suggestions
1. **Role-Based Access Control (RBAC)**: Middleware/decorator `@role_required('super_admin', 'event_admin')` for endpoints. Check user_roles for event_id if scoped.
2. **Pagination & Filtering**: All list APIs POST body `{search: str, type: enum?, zone_id?, event_id?, page: int=1, limit: int=20}` return `{data: [...], total: int, page, limit}`.
3. **QR Code Generation**: API `/api/v1/profile/qr` GET returns PNG/SVG QR(access_token). Frontend displays.
4. **Profile API**: `/api/v1/profile` GET full user + current roles/events/companies/connections count.
5. **Scan Validation API**: `/api/v1/scan/validate` POST `{access_token, zone_id, event_id?, action: 'enter'|'exit'}` → validate role/location/status, add EventAttendance/ZoneScans records, return status.
6. **Dashboard Stats**: `/api/v1/dashboard` GET role-specific: events count, scans today, connections pending etc.
7. **Audit Logs**: created_by/updated_by FK user.id all models.
8. **Event Status**: published bool, capacity int.
9. **Zone Capacity/Status**: current occupancy from scans.
10. **Connections Mutual**: add request → accept API, notifications WS later.

## Tech
- Frontend: React/Vue + QR scanner (html5-qrcode), cam access.
- Rate Limit: flask-limiter scans.
- WS: flask-socketio real-time scans/connections.
- Tests: pytest CRUD auth.
- Deploy: Docker + nginx reverse, Postgres pg_bouncer.

Approve/reject ideas, then implement APIs per plan.