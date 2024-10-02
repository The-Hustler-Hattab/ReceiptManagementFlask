from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Integer, Column, Float, Date, String, DateTime
from app import Constants, app
from app.model.db.receipts_alchemy import Base, session
from app.service.azure_blob import AzureBlobStorage, BlobType

logger = app.logger
logger.name = 'LLCIncome'
@dataclass
class LLCIncome(Base):
    __tablename__ = 'LLC_INCOME'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(500), nullable=False)
    gross_revenue = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    net_revenue = Column(Float, nullable=False)
    comment = Column(String(1000), nullable=True)
    proof_of_income_file_path = Column(String(500), nullable=True)
    created_at: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    created_by = Column(String, nullable=False)
    received_at: DateTime = Column(DateTime, nullable=False)



    def save_income(self) -> Column[int]:
        """Save the current instance to the database."""
        try:
            session.add(self)
            session.commit()
            logger.info(f"Successfully saved LLCIncome record with ID: {self.id}")
            return self.id
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def get_all() -> list:
        """Get all LLCIncome records from the database."""
        try:
            return session.query(LLCIncome).all()
        except Exception as e:
            logger.error(f"Failed to retrieve records: {e}")
            raise e



    @staticmethod
    def delete_by_id(record_id: int) -> bool:
        """Delete an LLCIncome record by ID."""
        try:
            # Fetch the record by ID
            record = session.query(LLCIncome).filter(LLCIncome.id == record_id).first()
            if record:
                if record.proof_of_income_file_path:
                    try:
                        AzureBlobStorage.delete_file_blob(record.proof_of_income_file_path, BlobType.INCOME_BLOB)
                    except Exception as e:
                        logger.error(f"Failed to delete file '{record.proof_of_income_file_path}' from Azure Blob Storage: {e}")

                session.delete(record)
                session.commit()
                logger.info(f"Successfully deleted LLCIncome record with ID: {record_id}")
                return True
            else:
                logger.warning(f"Record with ID: {record_id} not found")
                return False
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete record with ID: {record_id}, Error: {e}")
            raise e



    def to_dict(self):
        """Convert LLCIncome instance to dictionary format."""
        return {
            "id": self.id,
            "source": self.source,
            "gross_revenue": self.gross_revenue,
            "tax": self.tax,
            "net_revenue": self.net_revenue,
            "comment": self.comment,
            "proof_of_income_file_path": self.proof_of_income_file_path,
            "created_at": self.created_at.strftime("%Y-%m-%d") if self.created_at else None,
            "created_by": self.created_by,
            "received_at": self.received_at.strftime("%Y-%m-%d") if self.received_at else None,
        }