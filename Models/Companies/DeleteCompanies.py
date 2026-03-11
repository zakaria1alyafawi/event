from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .Companies import CompaniesModel
import logging
from datetime import datetime

logger = logging.getLogger('Models.Companies.DeleteCompanies')

class DeleteCompanies(BaseCRUD):
    """
    Class to handle soft deleting records from the companies table.
    """
    def __init__(self, session):
        super().__init__(session, CompaniesModel)

    def delete(self, id):
        """
        Soft delete a CompaniesModel record by ID.
        """
        id = validate_uuid(id, 'id')
        company = self.session.query(CompaniesModel).filter(CompaniesModel.id == id).first()
        if not company:
            logger.warning(f'Company {id} not found.')
            return False
        company.deleted_at = datetime.utcnow()
        try:
            self.session.commit()
            logger.info(f'Company {id} soft deleted.')
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f'Failed to delete company: {str(e)}')
            return False
