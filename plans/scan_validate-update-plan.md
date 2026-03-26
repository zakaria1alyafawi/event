# Scan Validate API Update Plan

## Goal
Update [`API/routes/security/scan_validate.py`](API/routes/security/scan_validate.py) to support security selecting **event mode** OR **zone mode** + action ('enter'/'exit'), then scanning multiple QR (access_token) with fixed target/action. Toggle logic based on **latest record.action == requested action** → deny; else insert new record. Separate tables: EventAttendance for event_id, ZoneScans for zone_id.

## Body Changes
Require:
- `access_token`: UUID* (QR)
- `action`: 'enter'|'exit'*
- Exactly **one** of:
  - `event_id`: UUID* (event mode)
  - `zone_id`: UUID* (zone mode)

Error if both/neither/missing required.

## Retained Checks (Essential Security)
- Auth token → scanner_id + `security` role ([`RetrieveUserRoles.has_role_name`](Models/UserRoles/RetrieveUserRoles.py))
- User = [`RetrieveUsers.get_by_access_token`](Models/Users/RetrieveUsers.py) active?
- Target exists (event/zone)
- User roles: exhibitor_staff/visitor for target event (keep)
- User company in target companies (keep)

## New Toggle Logic (Core Change)
For **event mode** (`event_id`):
1. latest = [`RetrieveEventAttendance.get_last_attendance`](Models/EventAttendance/RetrieveEventAttendance.py:52)(user.id, event_id)
2. if latest and latest.action == action: deny `already_${action}` (400)
3. else: [`AddEventAttendance.record_scan`](Models/EventAttendance/AddEventAttendance.py:16)(user.id, event_id, action, scanner_id)

For **zone mode** (`zone_id`):
1. latest = [`RetrieveZoneScans.get_last_scan`](Models/ZoneScans/RetrieveZoneScans.py:52)(user.id, zone_id)
2. if latest and latest.action == action: deny `already_${action}_zone`
3. Capacity: if zone.capacity and [`get_zone_occupancy`](Models/ZoneScans/RetrieveZoneScans.py:61)(zone_id) >= capacity: deny `capacity_full`
4. else: [`AddZoneScans.record_scan`](Models/ZoneScans/AddZoneScans.py:16)(user.id, zone_id, action, scanner_id)

**No cross-recording**: Event mode → only EventAttendance; Zone → only ZoneScans.

## All Cases (Toggle Table)
| Latest Action | No Latest | Request 'enter' | Request 'exit' |
|---------------|-----------|-----------------|---------------|
| None         | Allow enter | Allow (insert enter) | Allow (insert exit)?<br/>**Logic: treat as out → allow** |
| 'enter'      | -         | **Deny** already_in | Allow (insert exit) |
| 'exit'       | -         | Allow (insert enter) | **Deny** already_out |

## Flow Diagram
```mermaid
flowchart TD
    Start[POST /scan_validate<br/>{access_token*, action*, event_id? zone_id?}]
    Auth[Auth + security role]
    Parse[Validate body:<br/>exactly one target_id]
    User[Get user by access_token<br/>active?]
    Target[Get event/zone exists<br/>roles/company ok?]
    alt event_id
        LastE[Last EventAttendance<br/>user+event desc scanned_at]
    else zone_id
        LastZ[Last ZoneScans<br/>user+zone desc]
        Cap[occupancy < capacity?]
    end
    Toggle{latest.action == action?}
    alt Yes
        Deny[400 already_${action}]
    else
        Record[Insert record<br/>target table]
        Succ[200 success_ok<br/>user preview]
    end
```

## Implementation Todos
- Update body parsing/validation (XOR event/zone).
- Branch if event_id vs zone_id.
- Replace dual checks/records with single-table toggle.
- Capacity only zone.
- Update responses: status `event_enter_ok` / `zone_exit_ok` etc.
- Log mode (event/zone).
- Update [`openapi.yaml`](openapi.yaml) / [`plans/api-docs.md`](plans/api-docs.md).

## Files to Edit (Code Mode)
- [`scan_validate.py`](API/routes/security/scan_validate.py): Main logic.
- Optionally models if new methods (get_last_* exist).

Approve? Changes?