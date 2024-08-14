from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Numeric, String, DateTime

from app.model.db.receipts_alchemy import Base, session


class SherifSales:
    file_hash: str
    file_path: str
    file_name: str
    pages_size: int
    sherif_sale_date: datetime

    def __init__(self, file_hash: str, file_path: str, file_name: str, pages_size: int,
                 sherif_sale_date: datetime = None):
        self.file_hash = file_hash
        self.file_path = file_path
        self.file_name = file_name
        self.pages_size = pages_size
        self.sherif_sale_date = sherif_sale_date

    def convert_to_sherif_sale_alchemy(self) -> object:
        return SherifSale(file_hash=self.file_hash, file_path=self.file_path, file_name=self.file_name,
                          page_size=self.pages_size,
                          sherif_sale_date=self.sherif_sale_date
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
    sherif_sale_date: DateTime = Column(DateTime, nullable=False)

    @staticmethod
    def save_sherif_sale_to_db(sherif_sale: SherifSales) -> None:
        try:
            # Create an EmailCreds object
            alchemy_sherif_sale = sherif_sale.convert_to_sherif_sale_alchemy()
            # Add the object to the session
            session.add(alchemy_sherif_sale)
            # Commit the session to persist the object in the database
            session.commit()
            print("[+] Sherif Sale saved to db")
        except Exception as e:
            session.rollback()
            print(f'Error committing to the db: {e}')
            raise e
