''' 
UserRoles Module
------------------
This module contains the SQLAlchemy model and CRUD operations for the user_roles table.

Contents:
    - UserRoles: The table definition.
    - AddUserRoles: Logic for adding new records.
    - DeleteUserRoles: Logic for deleting records.
    - RetrieveUserRoles: Logic for retrieving records.
    - UpdateUserRoles: Logic for updating records.
'''

# Import the table model
from .UserRoles import UserRolesModel

# CRUD classes
from .AddUserRoles import AddUserRoles
from .DeleteUserRoles import DeleteUserRoles
from .RetrieveUserRoles import RetrieveUserRoles
from .UpdateUserRoles import UpdateUserRoles

__all__ = [
    'UserRolesModel',
    'AddUserRoles',
    'DeleteUserRoles',
    'RetrieveUserRoles',
    'UpdateUserRoles',
]
