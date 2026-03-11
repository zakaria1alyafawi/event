''' 
Events Module
------------------
This module contains the SQLAlchemy model and CRUD operations for the events table.

Contents:
    - Events: The table definition.
    - AddEvents: Logic for adding new records.
    - DeleteEvents: Logic for deleting records.
    - RetrieveEvents: Logic for retrieving records.
    - UpdateEvents: Logic for updating records.
'''

# Import the table model
from .Events import EventsModel

# CRUD classes
from .AddEvents import AddEvents
from .DeleteEvents import DeleteEvents
from .RetrieveEvents import RetrieveEvents
from .UpdateEvents import UpdateEvents

__all__ = [
    'EventsModel',
    'AddEvents',
    'DeleteEvents',
    'RetrieveEvents',
    'UpdateEvents',
]
