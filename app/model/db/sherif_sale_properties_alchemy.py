from datetime import datetime
from typing import List, Union

from sqlalchemy import Column, Numeric, String, DateTime

from app.model.db.receipts_alchemy import Base, session


class Property:
    sale: str
    case_number: str
    sale_type: str
    status: str
    tracts: str
    cost_tax_bid: str
    plaintiff: str
    attorney_for_plaintiff: str
    defendant: str
    property_address: str
    municipality: str
    parcel_tax_id: str
    comments: str
    SHERIEF_SALE_CHILD_ID: int
    zillow_link: str

    def __init__(self, sale: str = "", case_number: str = "", sale_type: str = "", status: str = "",
                 tracts: str = "", cost_tax_bid: str = "", plaintiff: str = "",
                 attorney_for_plaintiff: str = "", defendant: str = "", property_address: str = "",
                 municipality: str = "", parcel_tax_id: str = "", comments: str = ""):
        self.sale = sale
        self.case_number = case_number
        self.sale_type = sale_type
        self.status = status
        self.tracts = tracts
        self.cost_tax_bid = cost_tax_bid
        self.plaintiff = plaintiff
        self.attorney_for_plaintiff = attorney_for_plaintiff
        self.defendant = defendant
        self.property_address = property_address
        self.municipality = municipality
        self.parcel_tax_id = parcel_tax_id
        self.comments = comments

    def __str__(self):
        return (f"Property(sale={self.sale}, case_number={self.case_number}, sale_type={self.sale_type}, "
                f"status={self.status}, tracts={self.tracts}, cost_tax_bid={self.cost_tax_bid}, "
                f"plaintiff={self.plaintiff}, attorney_for_plaintiff={self.attorney_for_plaintiff}, "
                f"defendant={self.defendant}, property_address={self.property_address}, "
                f"municipality={self.municipality}, parcel_tax_id={self.parcel_tax_id}, comments={self.comments})")
    def convert_property_sherif_sale_alchemy(self) -> object:
        return PropertySherifSale(sale=self.sale, case_number=self.case_number, sale_type=self.sale_type,
                                  status=self.status, tracts=self.tracts, cost_tax_bid=self.cost_tax_bid,
                                  plaintiff=self.plaintiff, attorney_for_plaintiff=self.attorney_for_plaintiff,
                                  defendant=self.defendant, property_address=self.property_address,
                                  municipality=self.municipality, parcel_tax_id=self.parcel_tax_id,
                                  comments=self.comments, SHERIEF_SALE_CHILD_ID=self.SHERIEF_SALE_CHILD_ID,
                                  zillow_link=self.zillow_link)

class PropertySherifSale(Base):
    __tablename__ = 'SHERIEF_SALE_PROPERTY_TABLE'

    id: int = Column(Numeric, primary_key=True, nullable=False,autoincrement=True)
    sale: str = Column(String(255), nullable=False)
    case_number: str = Column(String(255), nullable=False)
    sale_type: str = Column(String(255), nullable=False)
    status: str = Column(String(255), nullable=False)
    tracts: str = Column(String(255), nullable=False)
    cost_tax_bid: str = Column(String(255), nullable=False)
    plaintiff: str = Column(String(255), nullable=False)
    attorney_for_plaintiff: str = Column(String(255), nullable=False)
    defendant: str = Column(String(255), nullable=False)
    property_address: str = Column(String(255), nullable=False)
    municipality: str = Column(String(255), nullable=False)
    parcel_tax_id: str = Column(String(255), nullable=False)
    comments: str = Column(String(255), nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    created_by: str = Column(String(200), nullable=False, default="SherifSale")
    SHERIEF_SALE_CHILD_ID: int = Column(Numeric, nullable=False)
    zillow_link: str = Column(String(300), nullable=True)

    @staticmethod
    def save_sherif_sale_to_db(property: Property) -> int:
        try:
            # Create an EmailCreds object
            alchemy_sherif_sale = property.convert_property_sherif_sale_alchemy()
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
    def save_all_sherif_sales_to_db(properties: List[Union[Property, 'PropertySherifSale']] ) -> None:
        try:
            # Iterate over the list of Property objects
            for property in properties:
                if isinstance(property, PropertySherifSale):
                    session.add(property)
                else:
                    # Convert and add each Property to the session
                    property_sherif_sale = property.convert_property_sherif_sale_alchemy()
                    session.add(property_sherif_sale)

            # Commit the session to persist all objects in the database
            session.commit()
            print("[+] All Sherif Sales saved to db")
        except Exception as e:
            # Rollback in case of any error
            session.rollback()
            print(f'Error committing the list to the db: {e}')
            raise e
    @staticmethod
    def get_all_by_tract(count: str) -> List['PropertySherifSale']:
        try:
            properties = session.query(PropertySherifSale).filter(PropertySherifSale.tracts == count
                                                                  ).all()
            return properties
        except Exception as e:
            print(f'Error fetching properties: {e}')
            raise e