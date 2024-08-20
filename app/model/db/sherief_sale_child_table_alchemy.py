from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Numeric, String, DateTime

from app.model.db.receipts_alchemy import Base, session


class SherifSalesChild:
    file_hash: str
    file_path: str
    file_name: str
    SHERIFF_SALE_DATE: datetime
    SHERIEF_SALE_MASTER_ID: int
    id: int

    def __init__(self, file_hash: str, file_path: str, file_name: str, SHERIEF_SALE_MASTER_ID: int,
                 SHERIFF_SALE_DATE: datetime = None):
        self.file_hash = file_hash
        self.file_path = file_path
        self.file_name = file_name
        self.SHERIFF_SALE_DATE: datetime = SHERIFF_SALE_DATE
        self.SHERIEF_SALE_MASTER_ID: int = SHERIEF_SALE_MASTER_ID

    def convert_to_sherif_sale_alchemy(self) -> object:
        return SherifSaleChild(file_hash=self.file_hash, file_path=self.file_path, file_name=self.file_name,
                               SHERIFF_SALE_DATE=self.SHERIFF_SALE_DATE,
                               SHERIEF_SALE_MASTER_ID=self.SHERIEF_SALE_MASTER_ID
                               )

    def to_dict(self):
        return {
            "file_hash": self.file_hash,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "SHERIFF_SALE_DATE": self.SHERIFF_SALE_DATE.isoformat() if isinstance(self.SHERIFF_SALE_DATE,
                                                                                  datetime) else self.SHERIFF_SALE_DATE,
            "SHERIEF_SALE_MASTER_ID": self.SHERIEF_SALE_MASTER_ID,
            "id": self.id
        }


class SherifSaleChild(Base):
    __tablename__ = 'SHERIEF_SALE_CHILD_TABLE'

    id: int = Column(Numeric, primary_key=True, nullable=False)
    file_hash: str = Column(String(255), nullable=False)
    file_path: str = Column(String(255), nullable=False)
    file_name: str = Column(String(255), nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    created_by: str = Column(String(200), nullable=False, default="SherifSale")
    SHERIFF_SALE_DATE: DateTime = Column(DateTime, nullable=False)
    SHERIEF_SALE_MASTER_ID: int = Column(Numeric, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "file_hash": self.file_hash,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "created_by": self.created_by,
            "SHERIFF_SALE_DATE": self.SHERIFF_SALE_DATE.isoformat() if isinstance(self.SHERIFF_SALE_DATE,
                                                                                  datetime) else self.SHERIFF_SALE_DATE,
            "SHERIEF_SALE_MASTER_ID": self.SHERIEF_SALE_MASTER_ID
        }

    @staticmethod
    def save_sherif_sale_to_db(sherif_sale: SherifSalesChild) -> int:
        try:
            # Create an EmailCreds object
            alchemy_sherif_sale_child = sherif_sale.convert_to_sherif_sale_alchemy()
            # Add the object to the session
            session.add(alchemy_sherif_sale_child)
            # Commit the session to persist the object in the database
            session.commit()

            print(f"[+] Sherif Sale saved to db with id {alchemy_sherif_sale_child.id}")
            return alchemy_sherif_sale_child.id
        except Exception as e:
            session.rollback()
            print(f'Error committing to the db: {e}')
            raise e
