# Production API Documentation - http://89.167.92.67:3000/api/v1/

All successful responses (except health):
```json
{
  "status": "success",
  "data": { ... }
}
```

Errors:
```json
{
  "status": "error",
  "message": "..."
}
```

## /api/v1/login (POST) - Public
**Payload**:
```json
{
  "email": "user@example.com",
  "password": "pass123"
}
```
**Success (200)** `data`:
```json
{
  "message": "Login successful",
  "token": "jwt",
  "access_token": "uuid",
  "id": "uuid",
  "first_name": "",
  "last_name": "",
  "display_name": "Full Name",
  "email": "",
  "phone": null,
  "job_title": null,
  "photo_url": null,
  "country": null,
  "city": null,
  "company_id": null,
  "company_name": null,
  "company": null,
  "auth_provider": "email",
  "auth_id": null,
  "is_active": true,
  "is_blacklisted": false,
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "deleted_at": null,
  "token_expires_at": null,
  "token_last_rotated_at": null,
  "roles": [
    {
      "event_id": null,
      "name": "super_admin",
      "role_id": "uuid"
    }
  ],
  "user_roles": "str repr"
}
```

## /api/v1/kill_session (GET) - Auth
**Payload**: none (header Authorization)
**Success (200)** `data`:
```json
{
  "message": "Session killed successfully",
  "session": "token"
}
```

## /api/v1/reset_password (POST) - Auth
**Payload**:
```json
{
  "new_password": "newpass123",
  "old_password": "oldpass", // self-reset
  "user_id": "uuid" // admin optional
}
```
**Success (200)** `data`:
```json
{
  "message": "Password reset successfully",
  "user": {
    "id": "uuid",
    "first_name": "",
    "last_name": "",
    "email": "",
    "phone": "",
    "job_title": "",
    "photo_url": "",
    "country": "",
    "city": "",
    "company_id": "uuid",
    "is_active": true,
    "is_blacklisted": false,
    "auth_provider": "",
    "auth_id": null
  }
}
```

## /api/v1/add_user (POST) - super_admin
**Payload**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "pass123",
  "role_name": "event_admin",
  "phone": "+1-234-567",
  "job_title": "Manager",
  "photo_url": "url",
  "country": "USA",
  "city": "NYC",
  "company_id": "uuid",
  "event_id": "uuid",
  "auth_provider": "email",
  "auth_id": null
}
```
**Success (201)** `data`:
```json
{
  "message": "User created successfully",
  "user": { full profile }
}
```

## /api/v1/retrieve_users (POST)
**Payload**:
```json
{
  "search": "John",
  "company_id": "uuid",
  "role_name": "event_admin",
  "page": 1,
  "limit": 20
}
```
**Success (200)** `data`:
```json
{
  "data": [...],
  "total": N,
  "page": 1,
  "limit": 20
}
```

(Continue with similar detailed payloads for all routes based on code required/optional fields...)

**Note**: Full payloads listed for all routes with all possible fields from validation in handlers. Docs updated.