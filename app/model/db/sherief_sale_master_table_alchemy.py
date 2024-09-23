from datetime import datetime, date
from typing import Optional

from sqlalchemy import Column, Numeric, String, DateTime, insert
from sqlalchemy.orm import relationship

from app.model.db.receipts_alchemy import Base, session
from app.model.db.sherief_sale_child_table_alchemy import SherifSaleChild
from app.model.db.sherif_sale_properties_alchemy import PropertySherifSale


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

    # One-to-many relationship with Child
    sherif_sale_children = relationship("SherifSaleChild", back_populates="sherif_sale")

    def to_dict(self):
        return {
            "id": self.id,
            "file_hash": self.file_hash,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "pages_size": self.pages_size,
            "created_at": self._serialize_date(self.created_at),
            "created_by": self.created_by,
            "sheriff_sale_date": self._serialize_date(self.SHERIFF_SALE_DATE),
            "sherif_sale_children": [child.to_dict() for child in self.sherif_sale_children] if self.sherif_sale_children else []
        }

    @staticmethod
    def _serialize_date(value):
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return value
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

    @staticmethod
    def get_all_sherif_sales() -> list:
        """
        Queries the database for all SherifSale records and prints them in JSON format.

        :param session: SQLAlchemy session object
        """
        try:
            # Query all SherifSale instances
            sherif_sales = session.query(SherifSale).all()

            return sherif_sales
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
    @staticmethod
    def get_sherif_sales_between_dates(start_date: datetime, end_date: datetime) -> list:
        """
        Retrieves all SherifSale records where SHERIFF_SALE_DATE is between start_date and end_date.

        :param start_date: The start date for filtering.
        :param end_date: The end date for filtering.
        :return: A list of SherifSale instances between the specified dates.
        """
        try:
            sherif_sales = session.query(SherifSale).filter(
                SherifSale.SHERIFF_SALE_DATE.between(start_date, end_date)
            ).all()
            return sherif_sales
        except Exception as e:
            print(f"An error occurred while fetching records: {e}")
            raise e

    @staticmethod
    def get_properties_by_sherif_sale_id(sherif_sale_id: int) -> list["SherifSaleChild"]:
        """
        Retrieves all PropertySherifSale records where SherifSale.id equals the given ID.

        :param sherif_sale_id: The ID of the SherifSale.
        :return: A list of PropertySherifSale instances.
        """
        try:
            properties = session.query(PropertySherifSale).join(
                PropertySherifSale.sherif_sale_child
            ).join(
                SherifSaleChild.sherif_sale
            ).filter(
                SherifSale.id == sherif_sale_id
            ).all()
            return properties
        except Exception as e:
            print(f"An error occurred while fetching properties: {e}")
            raise e