''' 
Zones Module
------------------
This module contains the SQLAlchemy model and CRUD operations for the zones table.

Contents:
    - Zones: The table definition.
    - AddZones: Logic for adding new records.
    - DeleteZones: Logic for deleting records.
    - RetrieveZones: Logic for retrieving records.
    - UpdateZones: Logic for updating records.
'''

# Import the table model
from .Zones import ZonesModel

# CRUD classes
from .AddZones import AddZones
from .DeleteZones import DeleteZones
from .RetrieveZones import RetrieveZones
from .UpdateZones import UpdateZones

__all__ = [
    'ZonesModel',
    'AddZones',
    'DeleteZones',
    'RetrieveZones',
    'UpdateZones',
]
