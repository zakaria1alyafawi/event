''' 
Companies Module
------------------
This module contains the SQLAlchemy model and CRUD operations for the companies table.

Contents:
    - Companies: The table definition.
    - AddCompanies: Logic for adding new records.
    - DeleteCompanies: Logic for deleting records.
    - RetrieveCompanies: Logic for retrieving records.
    - UpdateCompanies: Logic for updating records.
'''

# Import the table model
from .Companies import CompaniesModel

# CRUD classes
from .AddCompanies import AddCompanies
from .DeleteCompanies import DeleteCompanies
from .RetrieveCompanies import RetrieveCompanies
from .UpdateCompanies import UpdateCompanies

__all__ = [
    'CompaniesModel',
    'AddCompanies',
    'DeleteCompanies',
    'RetrieveCompanies',
    'UpdateCompanies',
]
