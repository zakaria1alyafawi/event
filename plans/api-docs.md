# Event Management API Documentation

**Production Server**: http://89.167.92.67:3000  
**Local Development**: http://localhost:6000 (port 6000), Docker: http://localhost:3000 (maps to 6000)

Interactive Swagger UI: Open [`swagger.html`](swagger.html) (uses [`openapi.yaml`](openapi.yaml))

## /api/v1/login
**Method**: POST  
**Auth**: Public  
**Headers**: `Content-Type: application/json`  
**Body**:
```json
{
  \"email\": \"zakariaaalyafawi@gmail.com\",
  \"password\": \"Abcdef@12345\"
}
```
**cURL Example**:
```bash
curl -X POST http://89.167.92.67:3000/api/v1/login \\
  -H \"Content-Type: application/json\" \\
  -d '{\"email\": \"zakariaaalyafawi@gmail.com\", \"password\": \"Abcdef@12345\"}'
```
**Responses**:
- **200**: `{\"message\": \"Login successful\", \"token\": \"eyJ...\", \"user\": {\"first_name\": \"Zakaria\", \"last_name\": \"Alyafawi\", \"email\": \"...\"}}`
- **400/401**: `{\"message\": \"Invalid credentials\"}`

## /api/v1/add_tenant
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"first_name\": \"John\",
  \"last_name\": \"Doe\",
  \"email\": \"john.doe@company.com\",
  \"password\": \"SecurePass123!\",
  \"phone\": \"+1234567890\",
  \"job_title\": \"Staff\",
  \"photo_url\": \"https://example.com/photo.jpg\",
  \"country\": \"USA\",
  \"city\": \"NYC\",
  \"company_id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"auth_provider\": \"email\",
  \"auth_id\": null
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  # from login
curl -X POST http://89.167.92.67:3000/api/v1/add_tenant \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"first_name\": \"John\", \"last_name\": \"Doe\", \"email\": \"john@company.com\", \"password\": \"Secure123!\"}'
```
**Responses**:
- **201**: `{\"message\": \"Tenant user created successfully\", \"user\": {\"id\": \"uuid\", \"first_name\": \"John\", \"email\": \"john@company.com\", ...}}`
- **400**: `{\"message\": \"Missing required fields: email\"}` or duplicate email
- **401**: `{\"message\": \"Invalid token\"}`
- **500**: `{\"message\": \"Internal server error\"}`

**Notes**:
- Password hashed automatically.
- Unique email/phone checked.
- company_id optional FK.
- Super_admin can add to any company.

## /api/v1/add_user
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"first_name\": \"John\",
  \"last_name\": \"Doe\",
  \"email\": \"john.doe@company.com\",
  \"password\": \"SecurePass123!\",
  \"role_name\": \"event_admin\",
  \"phone\": \"+1234567890\",
  \"job_title\": \"Staff\",
  \"photo_url\": \"https://example.com/photo.jpg\",
  \"country\": \"USA\",
  \"city\": \"NYC\",
  \"company_id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"event_id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"auth_provider\": \"email\",
  \"auth_id\": null
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  # from login
curl -X POST http://89.167.92.67:3000/api/v1/add_user \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"first_name\": \"John\", \"last_name\": \"Doe\", \"email\": \"john@company.com\", \"password\": \"Secure123!\", \"role_name\": \"event_admin\"}'
```
**Responses**:
- **201**: `{\"message\": \"User created successfully\", \"user\": {\"id\": \"uuid\", \"first_name\": \"John\", \"email\": \"john@company.com\", \"roles\": [{\"name\": \"event_admin\", \"event_id\": null}], \"company_id\": null, \"is_active\": true, ...}}`
- **400**: `{\"message\": \"Missing required fields: role_name\"}` or `{\"message\": \"Invalid role_name: invalid_role\"}`
- **401**: `{\"message\": \"Invalid or expired token\"}`
- **500**: `{\"message\": \"Internal server error\"}`

**Notes**:
- Creates user via AddUsers, assigns role via RetrieveUserTypes.get_by_name + AddUserRoles.add_role (event_id optional).
- role_name: super_admin|event_admin|security|exhibitor_staff|visitor (must exist).
- Password auto-hashed, email/phone unique validated.
- company_id optional FK to companies.
- Requires super_admin auth (via middleware).
- Soft deletes, is_active=true by default.

## /api/v1/retrieve_users
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"search\": \"John\",
  \"company_id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"role_name\": \"event_admin\",
  \"page\": 1,
  \"limit\": 20
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/retrieve_users \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"page\":1, \"limit\":20, \"role_name\":\"event_admin\"}'
```
**Responses**:
- **200**: `{\"data\": [{\"id\":\"uuid\", \"first_name\":\"John\", \"company_name\":\"Acme\", \"roles\":[\"event_admin\"]}, ...], \"total\":50, \"page\":1, \"limit\":20}`
- **400**: `{\"message\": \"Invalid company_id\"}`
- **401**: `{\"message\": \"Invalid token\"}`

**Notes**:
- Lists active users (is_active=true, no deleted_at).
- Filters: search (first/last/email ilike), company_id exact, role_name (exists UserRoles+UserTypes.name).
- Joins company.name, user_roles.role.name (array).
- Paginated offset/limit, ordered created_at desc.
- Super_admin auth.

## /api/v1/get_user
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"id\": \"550e8400-e29b-41d4-a716-446655440000\"
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/get_user \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"id\": \"550e8400-e29b-41d4-a716-446655440000\"}'
```
**Responses**:
- **200**: `{\"user\": {\"id\":\"uuid\", \"first_name\":\"John\", \"company_name\":\"Acme\", \"roles\":[{\"name\":\"event_admin\", \"event_id\":null}], ...}}`
- **404**: `{\"message\": \"User not found or inactive\"}`
- **401**: `{\"message\": \"Invalid token\"}`

**Notes**:
- Single active user by ID with company/roles.
- Joins for full profile.

## /api/v1/update_user
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"first_name\": \"Johnny\",
  \"last_name\": \"Doe Jr\",
  \"email\": \"johnny.doe@company.com\",
  \"phone\": \"+1234567891\",
  \"password\": \"NewSecurePass123!\",
  \"job_title\": \"Senior Manager\",
  \"photo_url\": \"https://example.com/newphoto.jpg\",
  \"country\": \"USA\",
  \"city\": \"NYC\",
  \"company_id\": \"550e8400-e29b-41d4-a716-446655440001\",
  \"is_active\": true,
  \"is_blacklisted\": false,
  \"auth_provider\": \"email\",
  \"auth_id\": null
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/update_user \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"id\": \"uuid\", \"first_name\": \"Johnny\", \"job_title\": \"Manager\"}'
```
**Responses**:
- **200**: `{\"message\": \"User updated successfully\", \"user\": {... full profile}}`
- **400**: `{\"message\": \"Email already exists\"}` (unique constraint)
- **404**: `{\"message\": \"User not found or inactive\"}`
- **401**: `{\"message\": \"Invalid token\"}`

**Notes**:
- Partial update: first_name, last_name, email, phone, password (hashed), job_title, photo_url, country, city, company_id, is_active, is_blacklisted, auth_provider, auth_id.
- Validations/unique constraints applied (email/phone).
- display_name auto from first/last.
- Returns full updated profile with company/roles.

## /api/v1/delete_user
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"id\": \"550e8400-e29b-41d4-a716-446655440000\"
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/delete_user \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"id\": \"uuid\"}'
```
**Responses**:
- **200**: `{\"message\": \"User deleted successfully\"}`
- **404**: `{\"message\": \"User not found\"}`
- **401**: `{\"message\": \"Invalid token\"}`

**Notes**:
- Soft delete: is_active=false, deleted_at=now().
- Super_admin auth.

## /api/v1/retrieve_events
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"title\": \"Demo\",
  \"organizer_id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"published\": true,
  \"page\": 1,
  \"limit\": 20
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/retrieve_events \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"page\":1, \"limit\":10}'
```
**Responses**:
- **200**: `{\"data\": [{\"id\":\"uuid\", \"slug\":\"demo-event\", \"title\":\"Demo Event\", \"organizer_name\":\"Zakaria Alyafawi\", \"is_published\":true}, ...], \"total\":5, \"page\":1, \"limit\":10}`
- **400**: validation
- **401**: token

**Notes**:
- Lists events (deleted_at null).
- Filters: search (title ilike), organizer_id, published bool.
- Joins organizer_name (first+last).
- Ordered created desc.

## /api/v1/add_events
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"slug\": \"new-event-2024\",
  \"title\": \"New Event 2024\",
  \"description\": \"Description\",
  \"start_date\": \"2024-11-01\",
  \"end_date\": \"2024-11-03\",
  \"venue\": \"New Venue\",
  \"organizer_id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"is_published\": false
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/add_events \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"slug\": \"new-event\", \"title\": \"New Event\", \"start_date\": \"2024-11-01\", \"end_date\": \"2024-11-03\", \"venue\": \"Venue\", \"organizer_id\": \"uuid\"}'
```
**Responses**:
- **201**: `{\"message\": \"Event created successfully\", \"event\": {\"id\":\"uuid\", \"slug\":\"new-event\", \"organizer_name\":\"Zakaria Alyafawi\", ...}}`
- **400**: slug exists, dates invalid
- **401**: token

**Notes**:
- Required: slug (uq), title, start_date < end_date, venue, organizer_id.
- Optional: description, is_published false.
- Joins organizer_name.

## /api/v1/update_events
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"title\": \"Updated Title\",
  \"venue\": \"Updated Venue\",
  \"is_published\": true
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/update_events \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"id\": \"uuid\", \"title\": \"Updated\", \"is_published\": true}'
```
**Responses**:
- **200**: `{\"message\": \"Event updated successfully\", \"event\": {...}}`
- **400**: slug uq violation
- **404**: not found
- **401**: token

**Notes**:
- Partial update (slug title desc dates venue organizer published).
- Slug uq validated.
- Full response with organizer_name.

## /api/v1/delete_events
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"id\": \"550e8400-e29b-41d4-a716-446655440000\"
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/delete_events \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"id\": \"uuid\"}'
```
**Responses**:
- **200**: `{\"message\": \"Event deleted successfully\"}`
- **404**: not found
- **401**: token

**Notes**:
- Soft delete: deleted_at = now().

## /api/v1/retrieve_zones
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"search\": \"Main\",
  \"event_id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"page\": 1,
  \"limit\": 20
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/retrieve_zones \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"page\":1, \"limit\":10, \"event_id\": \"uuid\"}'
```
**Responses**:
- **200**: `{\"data\": [{\"id\":\"uuid\", \"name\":\"Main Hall\", \"code\":\"MH1\", \"event_name\":\"Demo Event\", \"capacity\":100, \"is_restricted\":false}, ...], \"total\":3, \"page\":1, \"limit\":10}`
- **400**: validation
- **401**: token

**Notes**:
- Lists zones (deleted_at null).
- Filters: search (name/code ilike), event_id.
- Joins event.name.
- Ordered created desc.

## /api/v1/add_zone
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"event_id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"name\": \"VIP Zone\",
  \"code\": \"VIP1\",
  \"capacity\": 50,
  \"is_restricted\": true,
  \"location_x\": 10,
  \"location_y\": 20
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/add_zone \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"event_id\": \"uuid\", \"name\": \"VIP\", \"code\": \"VIP1\", \"capacity\":50}'
```
**Responses**:
- **201**: `{\"message\": \"Zone created successfully\", \"zone\": {\"id\":\"uuid\", \"name\":\"VIP\", \"event_name\":\"Demo Event\", ...}}`
- **400**: code uq event, validation
- **401**: token

**Notes**:
- Required: event_id, name, code (uq per event).
- Optional: capacity, is_restricted false, location_x/y.
- Joins event_name.

## /api/v1/update_zone
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"name\": \"VIP Updated\",
  \"capacity\": 60
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/update_zone \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"id\": \"uuid\", \"capacity\":60}'
```
**Responses**:
- **200**: `{\"message\": \"Zone updated successfully\", \"zone\": {...}}`
- **400**: code uq violation
- **404**: not found
- **401**: token

**Notes**:
- Partial update fields (code uq event).
- Full response with event_name.

## /api/v1/delete_zone
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"id\": \"550e8400-e29b-41d4-a716-446655440000\"
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/delete_zone \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"id\": \"uuid\"}'
```
**Responses**:
- **200**: `{\"message\": \"Zone deleted successfully\"}`
- **404**: not found
- **401**: token

**Notes**:
- Soft delete: deleted_at = now().

## /api/v1/get_companies_by_zone
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"zone_id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"search\": \"Exhib\",
  \"page\": 1,
  \"limit\": 20
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/get_companies_by_zone \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"zone_id\": \"uuid\", \"page\":1}'
```
**Responses**:
- **200**: `{\"data\": [{\"id\":\"uuid\", \"name\":\"Exhib Co\", \"zone_name\":\"VIP\", \"event_name\":\"Demo\", ...}, ...], \"total\":10, \"page\":1, \"limit\":20}`
- **400**: invalid zone_id
- **401**: token

**Notes**:
- Companies in zone (zone_id exact, search name ilike).
- Joins zone.name, event.title.
- Paginated ordered created desc.

## /api/v1/qr
**Method**: POST  
**Auth**: Bearer token  
**Body**: {}
**Responses**:
- 200: `{\"qr_code\": \"data:image/png;base64,iVBORw0KGgo...\"}`

**Notes**: Gen QR PNG b64 for auth user access_token.

## /api/v1/get_user_by_access_token
**Method**: POST  
**Auth**: Bearer token  
**Body**: `{\"access_token\": \"uuid\"}`
**Responses**:
- 200: `{\"user\": profile}`
- 404: invalid token

**Notes**: Preview scanned user (get_by_access_token).

## /api/v1/retrieve_connections
**Method**: POST  
**Auth**: Bearer token  
**Body**: `{\"page\":1, \"limit\":20}`
**Responses**:
- 200: `{\"data\": [{\"email\", \"first_name\", \"company_name\", ...}], \"total\", \"page\", \"limit\"}`

**Notes**: Friends paginated ordered scanned desc.

## /api/v1/add_connection
**Method**: POST  
**Auth**: Bearer token  
**Body**: `{\"friend_access_token\": \"uuid\"}`
**Responses**:
- 201: `{\"message\": \"Added\", \"connection\": {\"id\", \"scanned_at\"}}`
- 400: duplicate/invalid

**Notes**: Scan friend QR → add mutual connection uq pair event.

## /api/v1/retrieve_companies
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"search\": \"Exhib\",
  \"event_id\": \"uuid\",
  \"zone_id\": \"uuid\",
  \"booth_number\": \"B10\",
  \"page\": 1,
  \"limit\": 20
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/retrieve_companies \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"page\":1, \"zone_id\": \"uuid\"}'
```
**Responses**:
- **200**: `{\"data\": [{\"id\":\"uuid\", \"name\":\"Exhib Co\", \"booth_number\":\"B10\", \"zone_name\":\"VIP\", \"event_name\":\"Demo\", ...}], \"total\":15, \"page\":1, \"limit\":20}`
- **400**: validation
- **401**: token

**Notes**:
- Lists companies (deleted_at null).
- Filters: search (name ilike), booth_number ilike, event_id, zone_id.
- Joins zone.name event.title.
- Ordered created desc.

## /api/v1/add_company
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"event_id\": \"uuid\",
  \"zone_id\": \"uuid\",
  \"name\": \"New Exhib\",
  \"booth_number\": \"B20\",
  \"slug\": \"new-exhib\",
  \"logo_url\": \"logo.jpg\"
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/add_company \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"event_id\": \"uuid\", \"zone_id\": \"uuid\", \"name\": \"New Co\"}'
```
**Responses**:
- **201**: `{\"message\": \"Company created successfully\", \"company\": {\"id\":\"uuid\", \"name\":\"New Co\", \"zone_name\":\"VIP\", \"event_name\":\"Demo\", ...}}`
- **400**: validation
- **401**: token

**Notes**:
- Required: event_id, zone_id, name.
- Optional: booth slug logo desc website industry email phone.
- Joins zone/event.

## /api/v1/update_company
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"id\": \"uuid\",
  \"name\": \"Updated Co\",
  \"booth_number\": \"B21\"
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/update_company \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"id\": \"uuid\", \"name\": \"Updated\"}'
```
**Responses**:
- **200**: `{\"message\": \"Company updated successfully\", \"company\": {...}}`
- **400**: validation
- **404**: not found
- **401**: token

**Notes**:
- Partial update.
- Full response zone/event names.

## /api/v1/delete_company
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"id\": \"uuid\"
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/delete_company \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"id\": \"uuid\"}'
```
**Responses**:
- **200**: `{\"message\": \"Company deleted successfully\"}`
- **404**: not found
- **401**: token

**Notes**:
- Soft delete deleted_at=now().

## /api/v1/qr
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**: {}
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/qr \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{}'
```
**Responses**:
- **200**: `{\"qr_code\": \"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...\"}`
- **401**: token

**Notes**:
- Generates QR PNG base64 for auth user access_token (scanable).
- qrcode lib backend.

## /api/v1/get_user_by_access_token
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"access_token\": \"uuid-from-QR\"
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/get_user_by_access_token \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"access_token\": \"uuid\"}'
```
**Responses**:
- **200**: `{\"user\": {\"id\":\"uuid\", \"first_name\":\"John\", \"photo_url\":\"...\", \"roles\":[...]} }`
- **404**: invalid/inactive token
- **401**: auth token

**Notes**:
- Preview scanned user profile (name/photo/role) before add/validate.
- get_by_access_token active not expired.

## /api/v1/retrieve_connections
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"page\": 1,
  \"limit\": 20
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/retrieve_connections \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"page\":1}'
```
**Responses**:
- **200**: `{\"data\": [{\"email\":\"friend@ex.com\", \"first_name\":\"Friend\", \"company_name\":\"Ex Co\", ...}], \"total\":10, \"page\":1, \"limit\":20}`
- **401**: token

**Notes**:
- Friends list paginated ordered scanned desc.
- Serialize email phone first last display job photo company_name.

## /api/v1/add_connection
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"friend_access_token\": \"uuid-from-QR\"
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/add_connection \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"friend_access_token\": \"uuid\"}'
```
**Responses**:
- **201**: `{\"message\": \"Connection added\", \"connection\": {\"id\":\"uuid\", \"scanned_at\":\"...\"} }`
- **400**: invalid friend/self duplicate
- **401**: token

**Notes**:
- Scan friend QR → get_by_access_token → AddConnections(auth.id, friend.id) uq pair event note optional.

## /api/v1/health
**Method**: GET  
**Auth**: Public  
**Headers**: None  
**Body**: None
**cURL Example**:
```bash
curl -X GET http://89.167.92.67:3000/health
```
**Responses**:
- **200**: `{\"status\": \"healthy\", \"db_connected\": true, \"table_count\": 15}`
- **500**: `{\"status\": \"unhealthy\", \"db_connected\": false, \"error\": \"DB connection failed\"}`

**Notes**:
- Performs health check: connects to DB, lists tables count.
- No authentication required.
- Note: /health (not /api/v1/health as HealthRoute.bp has url_prefix='/health' and may need registration).

## /api/v1/kill_session
**Method**: GET  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Authorization: Bearer <token>`  
**Body**: None
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X GET http://89.167.92.67:3000/api/v1/kill_session \\
  -H \"Authorization: Bearer $TOKEN\"
```
**Responses**:
- **200**: `{\"message\": \"Session killed successfully\", \"session\": \"<token>\"}`
- **400**: `{\"message\": \"Authorization must be provided in header, not query parameter\"}`
- **401**: `{\"message\": \"Authorization header required\"}` or `{\"message\": \"Invalid or expired token\"}`
- **404**: `{\"message\": \"Session not found for token\"}`
- **415**: `{\"message\": \"Content-Type must be application/json or omitted\"}`
- **500**: `{\"message\": \"Failed to kill session\"}` or `{\"message\": \"Internal server error\"}`

**Notes**:
- Deactivates the authenticated user's current session (Status=2 inactive).
- Identifies session using the token from Authorization header.
- GET request, no body required.

## /api/v1/reset_password
**Method**: POST  
**Auth**: `Authorization: Bearer <token>`  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"new_password\": \"NewSecurePass123!\",
  \"old_password\": \"OldPass123!\",  // required for self-reset
  \"user_id\": \"uuid\"  // optional for admin reset other user
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/reset_password \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"new_password\": \"NewSecurePass123!\", \"old_password\": \"OldPass123!\"}'
```
**Responses**:
- **200**: `{\"message\": \"Password reset successfully\", \"user\": {\"id\": \"uuid\", \"first_name\": \"John\", \"email\": \"john@example.com\", ...}}`
- **400**: `{\"message\": \"new_password is required\"}`, `{\"message\": \"user_id must be an integer\"}`, etc.
- **401**: `{\"message\": \"Invalid old password\"}` or `{\"message\": \"Invalid or expired token\"}`
- **403**: `{\"message\": \"Only super_admin can reset other users' passwords\"}`
- **404**: `{\"message\": \"Active user not found: uuid\"}`
- **415**: `{\"message\": \"Content-Type must be application/json\"}`
- **500**: `{\"message\": \"Failed to update password\"}` or `{\"message\": \"Internal server error\"}`

**Notes**:
- For self-reset (no user_id): requires valid old_password.
- Admin reset: user_id provided, requires super_admin role, no old_password.
- New password is automatically hashed.
- Returns updated user profile (no password field).

## /api/v1/scan_validate
**Method**: POST  
**Auth**: `Authorization: Bearer <token>` (requires 'security' role)  
**Headers**: `Content-Type: application/json`, `Authorization: Bearer <token>`  
**Body**:
```json
{
  \"access_token\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"zone_id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"event_id\": \"550e8400-e29b-41d4-a716-446655440000\",  // optional
  \"action\": \"enter\"  // or \"exit\"
}
```
**cURL Example**:
```bash
TOKEN=\"eyJ...\"  
curl -X POST http://89.167.92.67:3000/api/v1/scan_validate \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Bearer $TOKEN\" \\
  -d '{\"access_token\": \"uuid-qr\", \"zone_id\": \"uuid\", \"action\": \"enter\"}'
```
**Responses**:
- **200**: `{\"success\": true, \"status\": \"enter_ok\", \"message\": \"Enter successful\", \"user\": {\"first_name\": \"John\", \"photo_url\": \"https://...\", \"roles\": [\"visitor\", \"exhibitor_staff\"]}}`
- **400**: `{\"message\": \"access_token, zone_id, action required\"}`, `{\"message\": \"already_in_zone\"}` (status='already_in_zone'), `{\"message\": \"capacity_full\"}`, etc.
- **401**: `{\"message\": \"Invalid or expired token\"}`
- **403**: `{\"message\": \"Scanner must have security role\"}`, `{\"message\": \"User role not authorized for event\"}` (status='denied_role'), `{\"message\": \"User company not in event/zone\"}` (status='denied_company')
- **404**: `{\"message\": \"Zone not found\"}` or `{\"message\": \"Event not found\"}`
- **500**: `{\"message\": \"Internal server error\"}`

**Notes**:
- Used by security staff to validate and record user entry/exit to zones/events via QR access_token scan.
- Checks: scanner has 'security' role, user active with exhibitor_staff/visitor role for event, user's company assigned to event/zone, not already in/out, zone capacity.
- Automatically records ZoneScans and EventAttendance.
- event_id optional (uses zone.event_id if omitted).
- Returns basic user info for confirmation.

**Error Responses** (global):
- 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 405 Method Not Allowed, 429 Too Many Requests, 500 Internal Server Error, 503 Service Unavailable