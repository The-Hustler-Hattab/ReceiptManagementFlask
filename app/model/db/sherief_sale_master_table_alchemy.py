from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Numeric, String, DateTime, insert

from app.model.db.receipts_alchemy import Base, session


class SherifSales:
    file_hash: str
    file_path: str
    file_name: str
    pages_size: int
    SHERIFF_SALE_DATE: datetime

    def __init__(self, file_hash: str, file_path: str, file_name: str, pages_size: int,
                 SHERIFF_SALE_DATE: datetime = None):
        self.file_hash = file_hash
        self.file_path = file_path
        self.file_name = file_name
        self.pages_size = pages_size
        self.SHERIFF_SALE_DATE = SHERIFF_SALE_DATE

    def convert_to_sherif_sale_alchemy(self) -> object:
        return SherifSale(file_hash=self.file_hash, file_path=self.file_path, file_name=self.file_name,
                          pages_size=self.pages_size,
                          SHERIFF_SALE_DATE=self.SHERIFF_SALE_DATE
                          )


class SherifSale(Base):
    __tablename__ = 'SHERIEF_SALE_MASTER_TABLE'

    id: int = Column(Numeric, primary_key=True, nullable=False)
    file_hash: str = Column(String(255), nullable=False)
    file_path: str = Column(String(255), nullable=False)
    file_name: str = Column(String(255), nullable=False)
    pages_size: int = Column(Numeric, nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    created_by: str = Column(String(200), nullable=False, default="SherifSale")
    SHERIFF_SALE_DATE: DateTime = Column(DateTime, nullable=False)

    @staticmethod
    def save_sherif_sale_to_db(sherif_sale: SherifSales) -> int:
        try:
            # Create an EmailCreds object
            alchemy_sherif_sale = sherif_sale.convert_to_sherif_sale_alchemy()
            # Add the object to the session
            session.add(alchemy_sherif_sale)
            # Commit the session to persist the object in the database
            session.commit()
            
            print("[+] Sherif Sale saved to db")
            return alchemy_sherif_sale.id
        except Exception as e:
            session.rollback()
            print(f'Error committing to the db: {e}')
            raise e


