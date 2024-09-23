from datetime import datetime, date
from typing import Optional

from sqlalchemy import Column, Numeric, String, DateTime, text, select, not_, ForeignKey
from sqlalchemy.orm import relationship

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
    SHERIEF_SALE_MASTER_ID: int = Column(Numeric, ForeignKey('SHERIEF_SALE_MASTER_TABLE.id'), nullable=False)

    # Many-to-one relationship with SherifSale
    sherif_sale = relationship("SherifSale", back_populates="sherif_sale_children")

    # One-to-many relationship with Child
    sherif_sale_properties = relationship("PropertySherifSale", back_populates="sherif_sale_child")

    def __str__(self):
        return (f"SherifSaleChild(id={self.id}, file_hash='{self.file_hash}', file_path='{self.file_path}', "
                f"file_name='{self.file_name}', created_at={self.created_at}, created_by='{self.created_by}', "
                f"SHERIFF_SALE_DATE={self.SHERIFF_SALE_DATE}, SHERIEF_SALE_MASTER_ID={self.SHERIEF_SALE_MASTER_ID})")

    def to_dict(self):
        return {
            "id": self.id,
            "sherif_sale_master_id": self.SHERIEF_SALE_MASTER_ID,
            "file_hash": self.file_hash,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "created_at": self._serialize_date(self.created_at),
            "created_by": self.created_by,
            "sheriff_sale_date": self._serialize_date(self.SHERIFF_SALE_DATE),
            "sherif_sale_properties": [child.to_dict() for child in
                                       self.sherif_sale_properties] if self.sherif_sale_properties else []
        }

    @staticmethod
    def _serialize_date(value):
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return value

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

    @staticmethod
    def update_sheriff_sale_date_by_file_hash(file_hash: str, new_date: datetime) -> bool:
        try:
            # SQL statement to update the SHERIFF_SALE_DATE by file_hash
            sql = text("""
                UPDATE SHERIEF_SALE_CHILD_TABLE
                SET SHERIFF_SALE_DATE = :new_date
                WHERE file_hash = :file_hash
            """)

            # Execute the raw SQL with parameters
            result = session.execute(sql, {"new_date": new_date, "file_hash": file_hash})
            session.commit()

            if result.rowcount > 0:
                print(f"[+] SHERIFF_SALE_DATE updated for file hash {file_hash}")
                return True
            else:
                print(f"[-] No record found with file hash {file_hash}")
                return False
        except Exception as e:
            session.rollback()
            print(f"Error updating SHERIFF_SALE_DATE: {e}")
            raise e

    # @staticmethod
    # def get_unmatched_records_with_empty_sale_date(sale_date: str):
    #     try:
    #         # Raw SQL query
    #         sql = text("""
    #             SELECT * FROM SHERIEF_SALE_CHILD_TABLE ssct
    #             WHERE ssct.ID NOT IN (SELECT sspt.SHERIEF_SALE_CHILD_ID FROM SHERIEF_SALE_PROPERTY_TABLE sspt)
    #             AND ssct.SHERIFF_SALE_DATE = :sale_date
    #         """)
    #
    #         # Execute the raw SQL query with the provided sale_date parameter
    #         result = session.execute(sql, {"sale_date": sale_date}).fetchall()
    #
    #         # Manually construct SherifSaleChild objects from the query result
    #         records = []
    #         for row in result:
    #             record = SherifSaleChild(
    #                 id=row[0],  # Assuming 'id' is the first column
    #                 file_hash=row[1],  # Assuming 'file_hash' is the second column
    #                 file_path=row[2],  # Assuming 'file_path' is the third column
    #                 file_name=row[3],  # Assuming 'file_name' is the fourth column
    #                 created_at=row[4],  # Assuming 'created_at' is the fifth column
    #                 created_by=row[5],  # Assuming 'created_by' is the sixth column
    #                 SHERIFF_SALE_DATE=row[6],  # Assuming 'SHERIFF_SALE_DATE' is the seventh column
    #                 SHERIEF_SALE_MASTER_ID=row[7]  # Assuming 'SHERIEF_SALE_MASTER_ID' is the eighth column
    #             )
    #             records.append(record)
    #
    #         return records  # Returns a list of SherifSaleChild objects
    #     except Exception as e:
    #         session.rollback()
    #         print(f"Error executing the query: {e}")
    #         raise e
