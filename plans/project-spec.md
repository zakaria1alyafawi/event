# Project Specification: Event Management Platform

## Overview
Multi-tenant web platform for event management. Backend Flask API + Postgres ORM. Frontend (TBD React?) with cam QR scanner.

**Key Features**:
- JWT auth with DB sessions (opaque tokens)
- Hierarchical roles: super_admin > event_admin > security > exhibitor_staff/visitor
- Events/Zones/Companies CRUD (admin scoped)
- Users/Employees CRUD assign roles (tenant_management)
- QR scans for attendance/connections (security/staff)
- Networking connections scan QR
- Dashboard lists filters pagination POST body

## Requirements
### Users & Roles
- super_admin: full CRUD events zones companies users, assign roles
- event_admin: manage own events zones companies staff
- security: scan zones companies enter/exit
- exhibitor_staff: profile QR companies connections (event exhib)
- visitor: profile QR companies connections (attendee)

### Admin (super_admin)
- Home dashboard stats
- Employees page: list filter type company, add (fields + role event_id), update del
- Events page: list search name, add update del (slug title dates venue organizer)
- Zones page: list event, add update del (event name code)
- Companies page: list event zone, add update del (event zone name)

### Security
- Login → companies list search (exhib booths)
- Zones list select (frontend state enter/exit mode)
- Cam QR scan access_token → validate add EventAttendance ZoneScans (toggle state already_in denied_role capacity?)

### Staff/Visitor
- Login profile (info roles events)
- QR code (access_token image)
- Companies list filter zone name search
- Connections: scan QR friend → add, list friends info

## Tech & Logic
- All GET/CRUD POST body {id for up/del/get, filters page limit for list}
- Soft del deleted_at is_active
- Pagination {data[], total page limit}
- Role check join user_roles event scoped
- Scan logic: user active role match event/zone company, toggle enter/exit check last scan
- QR frontend scanner → access_token → API validate/add

## Models (Ready)
Users company_id roles join, Events organizer_id, Zones event_id, Companies event zone, Attendance Scans user scanner event/zone action time
