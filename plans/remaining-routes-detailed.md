# Remaining Routes Detailed

## Current Implemented
- tenant_management: users CRUD
- event: events CRUD
- zones: zones CRUD get_companies_by_zone
- companies: companies CRUD
- staff: qr get_user_by_access_token retrieve_connections add_connection

## Remaining (Priority High to Low)

### 1. Security Scan Validate
**Dir**: API/routes/security/scan_validate.py
**POST /scan_validate**
**Body**: {access_token*, zone_id*, event_id?, action 'enter'/'exit'}
**Logic** (api-plan 93-172):
1. user = RetrieveUsers.get_by_access_token(access_token) active not deleted blacklisted
2. zone = RetrieveZones.get_by_id(zone_id)
3. event = RetrieveEvents.get_by_id(event_id or zone.event_id)
4. user roles exhib/visitor match event companies zone companies
5. last_zone = RetrieveZoneScans.list(user.id zone_id desc1)
6. last_event = RetrieveEventAttendance.list(user.id event.id desc1)
7. toggle: enter if last enter no exit already_in_zone/event, exit if last exit already_out
8. AddZoneScans(user.id zone.id scanner=auth.id action now)
9. AddEventAttendance(user.id event.id scanner action)
Resp {success bool, status 'enter_ok'/'exit_ok'/'already_in_zone'/'denied_role'/'inactive', message, user {name photo role}, occupancy?}

### 2. Dashboard Stats
**Dir**: API/routes/dashboard/dashboard.py
**POST /dashboard**
**Body**: {}
**Logic**: role stats:
- super_admin: total events users companies scans
- event_admin: own events zones companies staff scans
- security: scans today zones companies
- staff: connections events companies profile stats
Resp {events_count, users_count, scans_today, connections_pending etc}

### 3. Connections Delete
**Dir**: API/routes/staff/delete_connection.py
**POST /delete_connection**
**Body**: {connection_id*}
**Logic**: DeleteConnections.delete(connection_id) soft

### 4. ZoneScans/EventAttendance CRUD (Admin/Internal)
**Dir**: API/routes/scans/
retrieve_zone_scans {user_id? zone_id? event_id? page} paginated
add_zone_scan (internal scan_validate calls)
etc if UI.

### 5. Password Reset Update (fix reset_password UserID int → UUID)
UpdateUsers.update UserID UUID.

## Vision
- Security: frontend mode conference/zone enter/exit → scan_validate toggle trace full (event zone scans).
- Staff: scan preview get_user_by_access_token → add_connection.
- Admin dashboard stats.
- Complete platform.

Implement scan_validate next.