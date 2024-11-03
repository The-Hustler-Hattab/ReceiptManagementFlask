import logging
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Integer, Column, Float, Date, String, DateTime
from app.model.db.receipts_alchemy import Base, session
from app.service.azure_blob import AzureBlobStorage, BlobType


logger = logging.getLogger('Contractors')



@dataclass
class Contractor(Base):
    __tablename__ = 'contractors'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    created_at: DateTime = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    created_by: str = Column(String(100), nullable=False)
    contractor_name: str = Column(String(200), nullable=False)
    contractor_skill: str = Column(String(500), nullable=False)
    job_cost: str = Column(String(50), nullable=True)
    phone_number: str = Column(String(50), nullable=False)
    comment: str = Column(String(900), nullable=True)
    quote_file_location: str = Column(String(300), nullable=True)

    def save_contractor(self) -> Column[int]:
        """Save the current instance to the database."""
        try:
            session.add(self)
            session.commit()
            logger.info(f"Successfully saved Contractor record with ID: {self.id}")
            return self.id
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def get_all() -> list:
        """Get all LLCIncome records from the database."""
        try:
            return session.query(Contractor).all()
        except Exception as e:
            logger.error(f"Failed to retrieve records: {e}")
            raise e

    @staticmethod
    def delete_by_id(record_id: int) -> bool:
        """Delete an Contractor record by ID."""
        try:
            # Fetch the record by ID
            record = session.query(Contractor).filter(Contractor.id == record_id).first()
            if record:
                if record.quote_file_location:
                    try:
                        AzureBlobStorage.delete_file_blob(record.quote_file_location, BlobType.CONTRACTOR_BLOB)
                    except Exception as e:
                        logger.error(f"Failed to delete file '{record.quote_file_location}' from Azure Blob Storage: {e}")

                session.delete(record)
                session.commit()
                logger.info(f"Successfully deleted Contractor record with ID: {record_id}")
                return True
            else:
                logger.warning(f"Record with ID: {record_id} not found")
                return False
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete record with ID: {record_id}, Error: {e}")
            raise e
    def to_dict(self):
        """Convert Contractor instance to dictionary format."""
        return {
            "id": self.id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "created_by": self.created_by,
            "contractor_name": self.contractor_name,
            "contractor_skill": self.contractor_skill,
            "job_cost": self.job_cost,
            "phone_number": self.phone_number,
            "comment": self.comment,
            "quote_file_location": self.quote_file_location,
        }