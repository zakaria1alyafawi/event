# Event Management Models Implementation Plan

## Schema Analysis
Tables in FK dependency order:
1. user_types (no FK)
2. users (company_id deferred)
3. events (organizer_id -> users)
4. zones (event_id -> events)
5. companies (event_id -> events, zone_id -> zones)
6. user_roles (user_id -> users, role_id -> user_types, event_id -> events)
7. event_attendance (user_id, scanner_id -> users, event_id -> events)
8. zone_scans (user_id, scanner_id -> users, zone_id -> zones)
9. connections (user_id, connected_to_id -> users, event_id -> events)

Enums:
- user_role: 'super_admin', 'event_admin', 'security', 'exhibitor_staff', 'visitor'
- scan_action: 'enter', 'exit'

## Key Changes to Existing
- Users: UUID PK, new fields (auth_provider, photo_url, access_token etc.), is_active BOOLEAN, deleted_at soft delete, no TenantID, company_id FK companies (deferred)
- Sessions: UserID UUID FK 'users.id' (update Column)
- DatabaseInitializer: new CREATE TYPE / ALTER for enums, seed user_types (id=uuid, name=each enum value), create_all order, seed super_admin user (email zakaria..., role super_admin)

## Model Package Template
For each folder Models/XXX/:
```
XXX/
├── __init__.py          # docs, from .XXX import Model, from .AddXXX import AddXXXs etc., __all__
├── XXX.py               # class XXXModel(Base): __tablename__='xxx', Columns (UUID PK default=server_default=text(\"gen_random_uuid()\"), TIMESTAMPTZ=Timestamp(timezone=True) default=func.now(), relationships), __table_args__=(UniqueConstraint, Index...)
├── AddXXX.py            # class AddXXXs(BaseCRUD): def add(**fields): validate + manual new_record or super.add
├── DeleteXXX.py         # class DeleteXXX(BaseCRUD): def delete(id): super.delete(id)
├── UpdateXXX.py         # class UpdateXXXs(BaseCRUD): def update(id, **kwargs): validate kwargs + super.update
├── RetrieveXXX.py       # class RetrieveXXX(BaseCRUD): def get_by_*(field/val), list_active etc.
└── test.py              # example usage
```

**UUID Handling**:
```python
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
```

**TIMESTAMPTZ**:
```python
from sqlalchemy import DateTime
created_at = Column(DateTime(timezone=True), server_default=func.now())
```

**Enum**:
Column(Enum('user_role', name='user_role'))

## Specific CRUD Methods per Table
**UserTypes**:
- RetrieveUserTypes.get_by_name(role_name), get_all_active()

**Users**:
- AddUsers.register(email, password, first_name, last_name...)
- RetrieveUsers.get_by_email(email), get_by_access_token(token), validate_login(email, pw), search_by_company(company_id), get_active_by_event_role(event_id, role)
- UpdateUsers.rotate_token(user_id), set_active(user_id, active=True), blacklist(user_id)

**UserRoles**:
- AddUserRoles.assign_role(user_id, role_name, event_id=None), get_available_roles(event_id)
- RetrieveUserRoles.get_user_roles(user_id, event_id=None), has_role(user_id, role_name, event_id)
- DeleteUserRoles.revoke_role(user_id, role_name, event_id)

**Events**:
- AddEvents.create_event(slug, title, start_date...)
- RetrieveEvents.get_by_slug(slug), get_upcoming(limit=10), get_by_organizer(organizer_id)

**Zones**:
- RetrieveZones.get_by_event(event_id), get_by_event_code(event_id, code)

**Companies**:
- RetrieveCompanies.get_by_event(event_id), get_by_zone(zone_id), search_by_name(event_id, name)

**EventAttendance**:
- AddEventAttendance.record_scan(user_id, event_id, action='enter', scanner_id=None, device_info={})

**ZoneScans**:
- AddZoneScans.record_scan(user_id, zone_id, action='enter', scanner_id=None)

**Connections**:
- AddConnections.connect(user_id, connected_to_id, event_id=None, note='')
- RetrieveConnections.get_connections_for_user(user_id, event_id=None)

Implement these as methods in respective Add/Retrieve classes.

## Dependency Graph
```mermaid
graph LR
    user_types --> users
    users --> events
    events --> zones
    zones --> companies
    companies -.->. users
    events --> user_roles
    user_types --> user_roles
    users --> user_roles
    users --> event_attendance
    events --> event_attendance
    users --> zone_scans
    zones --> zone_scans
    users --> connections
    events --> connections
```

## Implementation Order (Todo Matches)
Follow todo list. After Models complete, update API routes to use new CRUDs (future step).

## Seeding Example
[... same as before ...]

Ready for code implementation after approval.