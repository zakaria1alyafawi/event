"""
EventAttendance Module
----------------------
This module contains the SQLAlchemy model and CRUD operations for the event_attendance table.

Contents:
    - EventAttendance: The table definition.
    - AddEventAttendance: Logic for adding new records.
    - DeleteEventAttendance: Logic for deleting records.
    - RetrieveEventAttendance: Logic for retrieving records.
"""

# Import the table model
from .EventAttendance import EventAttendanceModel

# CRUD classes
from .AddEventAttendance import AddEventAttendance
from .DeleteEventAttendance import DeleteEventAttendance
from .RetrieveEventAttendance import RetrieveEventAttendance

__all__ = [
    'EventAttendanceModel',
    'AddEventAttendance',
    'DeleteEventAttendance',
    'RetrieveEventAttendance',
]
