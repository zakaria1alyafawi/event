'''
Users Module
------------------
This module contains the SQLAlchemy model and CRUD operations for the Users table.

Contents:
    - Users: The table definition.
    - AddUser: Logic for adding new records.
    - DeleteUser: Logic for deleting records.
    - RetrieveUsers: Logic for retrieving records.
    - UpdateUser: Logic for updating records.
'''

# Import the table model
from .Users import UserModel

# Placeholder for CRUD classes (to be implemented)
from .AddUser import AddUsers
from .DeleteUser import DeleteUser
from .RetrieveUsers import RetrieveUsers
from .UpdateUser import UpdateUsers

__all__ = [
    "UserModel",
    "AddUsers",
    "DeleteUser",
    "RetrieveUsers",
    "UpdateUsers",
]
