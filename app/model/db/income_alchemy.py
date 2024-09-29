from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Integer, Column, Float, Date, String, DateTime
from app import Constants, app
from app.model.db.receipts_alchemy import Base, session
import logging

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
