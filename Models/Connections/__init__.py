''' 
Connections Module
------------------
This module contains the SQLAlchemy model and CRUD operations for the connections table.

Contents:
    - Connections: The table definition.
    - AddConnections: Logic for adding new records.
    - DeleteConnections: Logic for deleting records.
    - RetrieveConnections: Logic for retrieving records.
    - UpdateConnections: Logic for updating records.
'''

# Import the table model
from .Connections import ConnectionsModel

# CRUD classes
from .AddConnections import AddConnections
from .DeleteConnections import DeleteConnections
from .RetrieveConnections import RetrieveConnections
from .UpdateConnections import UpdateConnections

__all__ = [
    'ConnectionsModel',
    'AddConnections',
    'DeleteConnections',
    'RetrieveConnections',
    'UpdateConnections',
]
