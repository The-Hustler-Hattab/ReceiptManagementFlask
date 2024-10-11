import logging
from datetime import datetime, date

from sqlalchemy import Integer, Column, String, Date, DateTime, text
from sqlalchemy.orm import relationship

from app.model.db.receipts_alchemy import Base, session

logger = logging.getLogger('PlaidInstitutionAccessTokens')

class PlaidInstitutionAccessTokens(Base):
    __tablename__ = 'plaid_institution_access_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    institution_name = Column(String(255), nullable=False)
    institution_id = Column(String(255), nullable=False)
    access_token = Column(String(255), nullable=False)
    item_id = Column(String(255), nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    created_by = Column(String(255), nullable=False)

    # One-to-many relationship with Child
    accounts = relationship("PlaidAccounts", back_populates="access_token")

    @staticmethod
    def _serialize_date(value):
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "institution_name": self.institution_name,
            "institution_id": self.institution_id,
            "created_at": self._serialize_date(self.created_at),
            "created_by": self.created_by,
            "accounts": [child.to_dict() for child in self.accounts] if self.accounts else []
        }

    @staticmethod
    def save_access_token_to_db(plaidInstitutionAccessTokens: 'PlaidInstitutionAccessTokens') -> int:
        try:
            session.add(plaidInstitutionAccessTokens)
            # Commit the session to persist the object in the database
            session.commit()
            logger.info("[+] plaidInstitutionAccessTokens saved to db")
            return plaidInstitutionAccessTokens.id

        except Exception as e:
            session.rollback()
            logger.info(f'Error committing to the db: {e}')
            raise e

    @staticmethod
    def get_all() -> list:
        """Get all LLCIncome records from the database."""
        try:
            return session.query(PlaidInstitutionAccessTokens).all()
        except Exception as e:
            logger.error(f"Failed to retrieve records: {e}")
            raise e

    @staticmethod
    def get_access_token_by_id(id: int) -> str:
        """Get the access token by the primary key `id`."""
        try:
            token_record = session.query(PlaidInstitutionAccessTokens).filter_by(id=id).first()
            if token_record:
                return token_record.access_token
            else:
                raise Exception(f"No access token found for id: {id}")
        except Exception as e:
            logger.error(f"Failed to retrieve access token: {e}")
            raise e

    @staticmethod
    def delete_by_id(id: int) -> bool:
        """Delete a record by its primary key `id` using raw SQL."""
        try:

            # Record exists, proceed to delete
            delete_query = text("DELETE FROM plaid_institution_access_tokens WHERE id = :id")
            session.execute(delete_query, {'id': id})
            session.commit()
            logger.info(f"[+] Record with id {id} has been deleted")
            return True


        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete record: {e}")
            raise e

