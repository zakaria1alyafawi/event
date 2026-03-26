# Frontend API Integration Plan

## Executive Summary
The React frontend prototype in `ConnectEvent Web App Design/` is nearly production-ready with:
- Correct API base URL (`http://89.167.92.67:3000/api/v1`).
- TypeScript interfaces matching API responses from [`plans/api-docs.md`](plans/api-docs.md) and [`plans/prod-api-docs.md`](plans/prod-api-docs.md).
- Full pages for all flows: Login/Register, Admin Dashboard/Users/Events/Zones/Companies, Security Scanner, Visitor/Connections.
- AuthContext with localStorage persistence.
- Mock API service (`src/app/services/api.ts`) simulating delays/real data.

**Integration Goal**: Replace mocks with real `fetch` calls, add `Authorization: Bearer ${token}` headers for protected endpoints, handle real errors/loading/toasts. Test each API/flow using super-admin credentials first, then role-specific.

**Key Challenges**:
- Register: Prototype assumes public `/add_user`, backend requires auth (super_admin). Solution: Admin-only via Users page; self-register visitors later via new endpoint.
- Scanner Preview: Prototype `GET /user/:access_token`, backend `POST /get_user_by_access_token {access_token}` (protected).
- QR: Prototype `GET /qr`, backend `POST /qr {}` → base64.
- Scan: Prototype `/zone_scan`, backend `/scan_validate`.

**Serve Frontend**:
```
cd "ConnectEvent Web App Design"
npm install
npm run dev
```
Opens http://localhost:5173 (Vite).

## Overall Architecture Flow
```mermaid
graph TD
    Login[LoginPage POST /login] -->|token user roles| LS[localStorage]
    Auth[AuthContext] -->|Bearer token| Protected[CRUD retrieve_* add_*]
    QR[QRModal POST /qr] -->|base64| Display[QR Display]
    Scanner[Security/Visitor Scanner] --> POST_get_user[POST /get_user_by_access_token {access_token}]
    Scanner -->|Security| POST_scan[POST /scan_validate {access_token zone_id action}]
    Scanner -->|Visitor| POST_add_conn[POST /add_connection {friend_access_token}]
    Pages[Pages Events/Zones/Companies/Users] -->|POST body {page limit search...}| Backend[Prod API Server]
    Backend -->|{data[] total}| Pages
```

## Per-API Integration Plan

### 1. Authentication (Public/Protected)
| Frontend Function | Backend Endpoint | Payload/Headers | Response | Notes |
|-------------------|------------------|-----------------|----------|-------|
| `api.login(email, pw)` | `POST /login` | `{email, password}` JSON | `{message, token, user{roles[]}}` | Store `token`/`user` in LS. Pre-filled super-admin. |
| `api.killSession()` | `GET /kill_session` | `Authorization: Bearer token` | `{message, session}` | Clear LS. |
| `api.register(...)` | N/A (protected `/add_user`) | - | - | **Adjust**: Remove public register or backend change. Use admin Users page. |

**Test**: Login super-admin → verify token works on protected.

### 2. QR Generation/Display
| Frontend | Backend | Payload | Response | Notes |
|----------|---------|---------|----------|-------|
| `api.getQRCode()` | `POST /qr` | `{}` JSON, Bearer | `{qr_code: base64}` | Use `qrcode.react` client-side if needed, but backend provides PNG b64. Update to POST. |

**Test**: POST /qr with token → display in QRCodeModal.

### 3. Events Page (CRUD)
| Action | Endpoint | Body | Response |
|--------|----------|------|----------|
| List | `POST /retrieve_events` | `{search?, organizer_id?, published?, page=1, limit=20}` | `{data[{id slug title...}], total, page, limit}` |
| Add | `POST /add_events` | `{slug*, title*, ...}` | `{message, event{...}}` |
| Update | `POST /update_events` | `{id*, ...}` | `{message, event}` |
| Delete | `POST /delete_events` | `{id*}` | `{message}` |

**Frontend**: EventsPage grid/search/add modal. Replace mocks.

### 4. Zones Page
Similar to Events:
- `POST /retrieve_zones {search?, event_id?, page, limit}`
- `POST /add_zone {event_id*, name*, code?, capacity?, ...}`
- Update/Delete.

Filter by event_id.

### 5. Companies Page
- `POST /retrieve_companies {search?, event_id?, zone_id?, booth_number?, page, limit}`
- `POST /add_company {event_id*, zone_id*, name*, ...}`
- Update/Delete.
- "Add Staff": `POST /add_user {..., company_id, role_name: 'exhibitor_staff'}`

### 6. User Management
- `POST /retrieve_users {search?, company_id?, role_name?, page, limit}`
- `POST /add_user {first_name*, ..., role_name*, event_id?, company_id?}`
- Update/Delete/Get single.

Role dropdown: super_admin, event_admin, security, exhibitor_staff, visitor.

### 7. Role-Specific Flows

**Security Scanner (`/security`)**:
- List zones/companies (retrieve_*).
- Scan → `POST /get_user_by_access_token {access_token}` → preview user.
- Validate: `POST /scan_validate {access_token*, zone_id*, event_id?, action: 'enter'|'exit'}` → `{success, status, message, user}`.

**Visitor Connections (`/visitor`, `/connections`)**:
- Companies/Zones tabs.
- Scan → `POST /get_user_by_access_token {access_token}` → preview → `POST /add_connection {friend_access_token}`.
- List: `POST /retrieve_connections {page, limit}` → `{data[{email first_name company_name...}], total}`.

## Step-by-Step Todo List
Will be created via `update_todo_list`.

## Testing Sequence
1. Serve frontend.
2. Login super-admin → Dashboard.
3. Create Event → Zones → Companies → Users (different roles).
4. Logout → Login new role → Test flows.
5. Security: Scan simulate → preview → validate.
6. Visitor: Scan connect → Connections list.

## Potential Backend Adjustments
- Public visitor register (`POST /register`).
- Match scanner endpoints if needed.

Ready for implementation in Code mode.