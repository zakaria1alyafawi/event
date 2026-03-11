# Event Management API Plan (Detailed)
## Conventions
- POST /api/v1/{domain}/{action} body JSON
- Add: all model columns (* req from AddClass, ? opt null ok)
- Update: {id* uuid, field1?, field2?...}
- Retrieve/List: {search:str?, filter fields uuid/str enum, page=1 limit=20}
- Delete: {id* uuid}
- Resp list: {data: [obj min], total:int, page, limit}
- Role guard: check user_roles has required role (event scoped event_id match?)
- Validation: AddClass handles, ValueError → 400
- Soft del: deleted_at = now()
## TenantManagement - super_admin
### POST /retrieve_users
**Body**:
- search: str? email/name like
- company_id: uuid?
- role_name: str? filter roles
- page: int=1
- limit: int=20
**Logic**: RetrieveUsers.list(active) filter company/role/search join user_roles user_types, paginate
**Resp**: {data: [{id, first_name, last_name, email, phone?, company_name?, roles:[name]}], total, page, limit}
### POST /add_user
**Body** (UserModel + role):
- first_name*: str max100
- last_name*: str max100
- email*: str unique max500
- password*: str min6
- phone?: str unique max50
- job_title?: str max200
- photo_url?: str max500
- country?: str max100
- city?: str max100
- company_id?: uuid FK companies
- auth_provider?: str default 'email'
- auth_id?: str
- role_name*: 'event_admin'|'security'|'exhibitor_staff'|'visitor'
- event_id?: uuid (role scope)
**Logic**:
1. adder = AddUsers(session)
2. new_user = adder.add(first_name, last_name, password, email, phone, job_title, photo_url...)
3. role_type = RetrieveUserTypes(session).get_by_name(role_name)
4. AddUserRoles(session).add_role(new_user.id, role_type.id, event_id)
**Resp 201**: {message: 'User created', user: full {id, first_name..., display_name auto, is_active true, created_at, company?, role: {name, event_id?}} }
### POST /update_user
**Body**:
- id*: uuid
- first_name?: str
- ... any UserModel field (password hashed)
**Logic**: UpdateUsers(session).update(id, **body no id)
**Resp**: updated user
### POST /delete_user
**Body**: {id*: uuid}
**Logic**: DeleteUser(session).delete(id) soft
**Resp**: {message: 'Deleted'}
### POST /get_user
**Body**: {id*: uuid}
**Logic**: RetrieveUsers.get_by_id(id)
**Resp**: full user + roles[]
## Events - super_admin event_admin
### POST /retrieve_events
**Body**: {search:title?, organizer_id uuid?, page limit}
**Logic**: RetrieveEvents.list filter search organizer
**Resp**: data [{id, slug, title, start_date, end_date, venue, organizer_name, published}]
### POST /add_events
**Body** EventsModel:
- slug*: str unique
- title*: str
- description?: str
- start_date*: datetime
- end_date*: datetime
- venue*: str
- organizer_id*: uuid event_admin
- published?: bool false
**Logic**: AddEvents(session).add(**body)
**Resp 201**: new event
### POST /update_events {id*, slug?, ...}
UpdateEvents.update
### POST /delete_events {id*}
DeleteEvents.delete soft
## Zones
Similar RetrieveZones body {event_id? search page}
AddZones event_id* name* code? str unique/event
UpdateZones {id*, event_id?, name?}
DeleteZones {id*}
## Companies
RetrieveCompanies {event_id? zone_id? search page}
AddCompanies event_id* zone_id* name*
UpdateCompanies {id*, ...}
DeleteCompanies {id*}
## Security
### POST /retrieve_companies {search? event_id? zone_id? page} exhib companies zone/event
### POST /retrieve_zones {event_id?} security assigned/avail
### POST /scan_validate
**Body**:
- access_token*: uuid QR
- zone_id*: uuid
- event_id?: uuid zone.event
- action*: 'enter'|'exit'
**Logic**:
1. user = RetrieveUsers.get_by_access_token(access_token)
2. if not user.is_active or deleted_at or blacklisted: denied
3. zone = RetrieveZones.get_by_id(zone_id)
4. event = RetrieveEvents.get_by_id(event_id or zone.event_id)
5. if user roles not exhib/visitor for event/zone companies: denied
6. last_scan = RetrieveZoneScans.list(user.id, zone_id order desc)
7. if action 'enter' and last 'enter' no 'exit': already_in
8. AddZoneScans(user.id, zone.id, scanner=auth_user.id, action)
9. AddEventAttendance(user.id, event.id, scanner, action)
**Resp**: {success: bool, message, user: {name photo role}, status: 'enter_ok'|'exit_ok'|'already_in'|'capacity_full?'|'denied'}
## Staff
### GET /profile resp full user roles events companies stats
### GET /qr resp image/png QR(access_token data:image/png;base64)
### POST /retrieve_companies {search? zone_id? event_id? page} exhib list
### POST /retrieve_connections {page limit} friends full profile
### POST /add_connection {friend_access_token*} get friend RetrieveUsers.access_token → if valid add Connections(user.id, friend.id, event_id?)
Approve plan.

# Event Management API Plan (Complete Detailed)

## Features Coverage
- Admin: profile home employees (CRUD filter type) zones companies events (CRUD search)
- Security: companies search zone select cam scan QR validate enter/exit event_attendance zone_scans
- Staff/Visitor: profile QR companies filter zone/name connections scan QR add list

All POST body, pagination, role guard.

## TenantManagement - super_admin
retrieve_users: join users companies user_roles user_types filter company_id role_name search (email first_name), active
add_user: AddUsers.add all fields, auto display_name is_active=true; RetrieveUserTypes.get_by_name(role_name); AddUserRoles.add_role(new.id, role.id, event_id); commit
update_user: UpdateUsers.update(id, **patch) hash password if
delete_user: DeleteUser.delete(id) soft deleted_at
get_user: RetrieveUsers.get_by_id(id) + join roles companies

## Events
retrieve_events: RetrieveEvents.list filter search title organizer_id published? active events
add_events: AddEvents.add slug title desc start end venue organizer_id published false
update_events: UpdateEvents.update
delete_events: DeleteEvents.delete soft

## Zones
retrieve_zones: RetrieveZones.list filter event_id search name code, join event
add_zones: AddZones.add event_id name code (uq event/code)
...

## Companies
retrieve_companies: RetrieveCompanies.list filter event_id zone_id search name, join zone event
add_companies: AddCompanies.add event_id zone_id name
...

## Security - security role
retrieve_companies: filter exhib companies event zone search (for scan booths)
retrieve_zones: list zones event_id? assigned? (user_roles event_admin? or all)
scan_validate full logic:
1. user = RetrieveUsers.get_by_access_token(access_token) or None denied
2. if not user.is_active or user.deleted_at or user.is_blacklisted: {'success':false, 'status':'inactive'}
3. zone = RetrieveZones.get_by_id(zone_id) or None
4. event = RetrieveEvents.get_by_id(event_id or zone.event_id)
5. if user.company_id not in event companies or zone companies: denied_role
6. last_zone_scan = RetrieveZoneScans.list(user.id, zone_id, order desc limit 1)
7. last_event_att = RetrieveEventAttendance.list(user.id, event.id desc 1)
8. if action=='enter':
  if last_zone_scan and last_zone_scan.action=='enter' and no exit: 'already_in_zone'
  if last_event_att.action=='enter' no exit: 'already_in_event'
  AddZoneScans(user.id, zone.id, scanner=auth_user.id, action='enter', created_at=now)
  AddEventAttendance(user.id, event.id, scanner=auth_user.id, action='enter')
  'enter_ok'
9. if 'exit':
  if last_zone_scan.action=='exit': 'already_out_zone'
  AddZoneScans ... 'exit'
  AddEventAttendance 'exit'
  'exit_ok'
Resp: {success:bool, status:str, message:str, user:{first_name photo role}, occupancy?}

## Staff
profile: RetrieveUsers.get_full_profile(auth_user.id) join roles companies events
qr: gen QR str(access_token) png base64 data: URI
retrieve_companies: exhib companies filter zone event search
retrieve_connections: RetrieveConnections.list(auth_user.id)
add_connection: friend_user = RetrieveUsers.get_by_access_token(friend_token)
if friend exhib/visitor event? AddConnections(auth_user.id, friend_user.id, event_id=now_event)

Dashboard /dashboard POST {} role stats: events count scans today connections etc.

Ready.