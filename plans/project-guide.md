# Event Management Platform Development Guide

## 1. Database Models (Models/*)
### Model Package Structure (e.g. Models/Users/)
- **`__init__.py`**: `from .Users import UserModel; from .AddUser import AddUsers; ... __all__ = [...]` docs contents.
- **`Users.py` / Model.py**: `class UserModel(Base): __tablename__ = 'users' id=UUID PK gen_random_uuid(), columns (email Text uq? phone Text uq? password_hash Text first_name String(100) ... company_id FK ondelete SET NULL access_token UUID uq token_expires_at DateTime is_active Bool true deleted_at DateTime created/updated DateTime now()`
  - `__table_args__ = (UniqueConstraint('email'), Index('idx_company', 'company_id'))`
  - rels: `company = relationship('CompaniesModel', back_populates='users') user_roles = relationship('UserRolesModel', back_populates='user')`
- **`AddUser.py`**: `class AddUsers(BaseCRUD): def add(first_name, email, password, ...): validate_string/email etc self.add(**data) @commit_transaction`
- **`RetrieveUsers.py`**: `class RetrieveUsers(BaseCRUD): def get_by_id/email/access_token: filter active not deleted first() def list_paginated(search, company_id, role_name, page, limit): query filter active, if company filter company_id, search or_ ilike, role exists UserRoles UserTypes.name, total count, options joinedload company user_roles.role order desc offset limit serialize list dict roles list names`
- **`UpdateUser.py`**: `class UpdateUsers(BaseCRUD): def update(id, **kwargs): validate if 'email' etc if 'password' hash del 'password', super().update`
- **`DeleteUser.py`**: `class DeleteUser(BaseCRUD): def delete(id): query filter id set is_active=False deleted_at=now commit`
- **`test.py`**: examples add get.

### Base Model
`Models/Base.py`: `Base = declarative_base()`

### BaseCRUD
`Models/BaseCRUD.py`: `__init__(session, model_class)` add(**) hash Password if 'Password', get_all list(active_only=True **filters), get_by_id, update(**), delete soft if Status else hard, @commit_transaction rollback log.

### Table Registration
`Models/DatabaseInitializer.py`: initialize_tables(engine): create_all per package Base.metadata order UserTypes Users Events Zones Companies UserRoles Attendance Scans Connections Sessions

initialize_records(session): CREATE TYPE user_role/scan_action ENUM, AddUserTypes.add 5, seed admin super_admin role, demo event.

main.py calls if !tables init.

### Error Handling
Utility validate_* raise ValueError(msg)

BaseCRUD commit_transaction catch SQLAlchemyError rollback log raise

Route try ValueError error_response(str(ve),400) except Exception 500 log

## 2. API Routes (API/routes/*/)
### BaseRoute
`base.py`: `__init__()` self.bp = Blueprint, self.auth_manager = AuthManager(), get_session() append g.sessions

register_routes(bp.route /endpoint POST)(self.handler)

Handler: session = self.get_session() auth_header token auth_result = self.auth_manager.authenticate_request(session, token) if not user_id data = json required_fields missing error parse optionals model = Model(session) result = model.method(**) serialize success_response({msg, data:result}, status)

### App Factory
`API/__init__.py`: create_app Flask DevelopmentConfig CORS /api/v1/* * register_blueprint(route.bp /api/v1) before_request g.sessions = [] teardown close g.sessions

### Auth
middleware/auth.py AuthManager generate_token(jwt.encode user_id exp HS256 SECRET) authenticate_request RetrieveSessions.get_by_token(token) check not expired/killed return user_id

before_request in app? No, per route.

## 3. Responses
utils/responses.py success_response(data, status=200) jsonify(data) 200 error_response(msg, status=400) jsonify({"message": msg}) status

## 4. Pagination Serialize
Model list_paginated: query filter total=count() options joinedload rels order offset limit all() list dict str(id) fields rel.name list roles etc return {"data":list, "total":, "page":, "limit":}

## 5. Validation
Utility validate_string max_length, uuid UUID(str), integer >0, bool str true/false 1/0, date isoformat, enum in list

Model add/update if 'field' validate

## 6. Soft Delete
deleted_at = now() or is_active=False

Filter query deleted_at.is_(None) is_active True

Delete set deleted_at now()

## 7. Seeding
DatabaseInitializer seed enums types admin role demo event

FORCE_SEED env

## 8. Deployment
docker-compose db postgres app build ports 5432 6000 .env DB_* SECRET_KEY

main.py daemon flask 6000 debug

Yes, follow this for new entities.