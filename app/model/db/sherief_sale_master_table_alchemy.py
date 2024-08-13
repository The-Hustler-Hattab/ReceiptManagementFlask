from datetime import datetime

from sqlalchemy import Column, Numeric, String, DateTime

from app.model.db.receipts_alchemy import Base


class SherifSale(Base):
    __tablename__ = 'SHERIEF_SALE_MASTER_TABLE'

    id: int = Column(Numeric, primary_key=True, nullable=False)
    file_hash: str = Column(String(255), nullable=False)
    file_path: str = Column(String(255), nullable=False)
    file_name: str = Column(String(255), nullable=False)
    pages_size: int = Column(Numeric, nullable=False)
    created_at: str = Column(DateTime, nullable=False, default=datetime.now)
    created_by: str = Column(String(200), nullable=False, default="SherifSale")
