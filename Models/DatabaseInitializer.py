import logging
from datetime import datetime, date
from sqlalchemy import text
from Models.UserTypes.UserTypes import Base as UserTypesBase
from Models.Users.Users import Base as UsersBase
from Models.Events.Events import Base as EventsBase
from Models.Zones.Zones import Base as ZonesBase
from Models.Companies.Companies import Base as CompaniesBase
from Models.UserRoles.UserRoles import Base as UserRolesBase
from Models.EventAttendance.EventAttendance import Base as EventAttendanceBase
from Models.ZoneScans.ZoneScans import Base as ZoneScansBase
from Models.Connections.Connections import Base as ConnectionsBase
from Models.Sessions.UserSessions import Base as SessionsBase
from Models.UserTypes.AddUserTypes import AddUserTypes
from Models.Users.RetrieveUsers import RetrieveUsers
from Models.Users.AddUser import AddUsers
from Models.UserTypes.RetrieveUserTypes import RetrieveUserTypes
from Models.UserRoles.AddUserRoles import AddUserRoles
from Models.Events.AddEvents import AddEvents
from Models.Events.RetrieveEvents import RetrieveEvents

logger = logging.getLogger("Models.DatabaseInitializer")

class DatabaseInitializer:
    """
    Class to handle initialization of database tables and seeding in correct order.
    """
    @staticmethod
    def initialize_tables(engine):
        """
        Create tables in FK dependency order.
        """
        try:
            UserTypesBase.metadata.create_all(engine)
            UsersBase.metadata.create_all(engine)
            EventsBase.metadata.create_all(engine)
            ZonesBase.metadata.create_all(engine)
            CompaniesBase.metadata.create_all(engine)
            UserRolesBase.metadata.create_all(engine)
            EventAttendanceBase.metadata.create_all(engine)
            ZoneScansBase.metadata.create_all(engine)
            ConnectionsBase.metadata.create_all(engine)
            SessionsBase.metadata.create_all(engine)
            logger.info("All tables created successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize tables: {e}")
            raise

    @staticmethod
    def initialize_records(session):
        """
        Create enums and seed data.
        """
        logger.info("=== Starting DatabaseInitializer.initialize_records ===")
        try:
            # Create enums
            enums = {
                'user_role': ['super_admin', 'event_admin', 'security', 'exhibitor_staff', 'visitor'],
                'scan_action': ['enter', 'exit']
            }
            for enum_name, values in enums.items():
                try:
                    session.execute(text(f"CREATE TYPE {enum_name} AS ENUM ({', '.join(repr(v) for v in values)})"))
                    session.commit()
                    logger.info(f'Created enum {enum_name}')
                except Exception:
                    session.rollback()
                    logger.info(f'Enum {enum_name} already exists')
                for val in values:
                    try:
                        session.execute(text(f"ALTER TYPE {enum_name} ADD VALUE IF NOT EXISTS '{val}'"))
                        session.commit()
                    except Exception:
                        session.rollback()
                        logger.debug(f'Value {val} already in {enum_name}')

            # Seed user_types
            user_types_data = [
                ('super_admin', 'full platform access'),
                ('event_admin', 'event organizer/manager'),
                ('security', 'gate/zone validators'),
                ('exhibitor_staff', 'company booth staff'),
                ('visitor', 'normal attendees')
            ]
            add_user_types = AddUserTypes(session)
            for name, desc in user_types_data:
                try:
                    add_user_types.add(name, desc)
                    logger.info(f'Seeded user_type {name}')
                except ValueError:
                    logger.info(f'UserType {name} already exists')
            logger.info("=== User types seeded ===")

            # Seed super admin user
            retrieve_users = RetrieveUsers(session)
            admin = retrieve_users.get_by_email('zakariaaalyafawi@gmail.com')
            if not admin:
                add_users = AddUsers(session)
                admin = add_users.add(
                    first_name='Zakaria',
                    last_name='Alyafawi',
                    email='zakariaaalyafawi@gmail.com',
                    password='Abcdef@12345'
                )
                logger.info(f'Seeded super admin user {admin.id}')
            logger.info(f"=== Admin user handled (exists or seeded): {admin.id if admin else 'None'} ===")

            # Assign super_admin role to admin (global)
            retrieve_user_types = RetrieveUserTypes(session)
            super_role = retrieve_user_types.get_by_name('super_admin')
            if super_role and admin:
                add_user_roles = AddUserRoles(session)
                try:
                    add_user_roles.add_role(admin.id, super_role.id)
                    logger.info('Assigned super_admin role to admin')
                except ValueError:
                    logger.info('Admin already has super_admin role')
            logger.info("=== Role assignment done ===")

            # Seed demo event organized by admin
            logger.info("=== Starting event seeding ===")
            logger.info(f"=== Creating RetrieveEvents, admin.id={admin.id if admin else None} ===")
            retrieve_events = RetrieveEvents(session)
            logger.info("RetrieveEvents created successfully")
            event = retrieve_events.get_by_slug('demo-event')
            logger.info(f"Demo event exists: {bool(event)}")
            if not event:
                logger.info("Adding demo event...")
                add_events = AddEvents(session)
                add_events.add(
                    slug='demo-event',
                    title='Demo Event 2024',
                    description='Sample event for testing platform features.',
                    start_date='2024-10-01',
                    end_date='2024-10-03',
                    venue='Demo Convention Center',
                    organizer_id=admin.id,
                    is_published=True
                )
                logger.info('Seeded demo event')
            else:
                logger.info('Demo event already exists')

            logger.info("=== initialize_records completed successfully ===")
        except Exception as e:
            session.rollback()
            logger.error(f'Failed to initialize records: {e}')
            raise

