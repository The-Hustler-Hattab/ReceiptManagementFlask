from datetime import datetime, date
from typing import List, Union

from sqlalchemy import Column, Numeric, String, DateTime, Text, func, text, ForeignKey
from sqlalchemy.orm import relationship

from app.model.db.receipts_alchemy import Base, session
from app.model.generic.zillow_model import ZillowModel


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

    zestimate: str
    zestibuck: str
    events: str
    schools: str
    year_built: str
    lot_size: str
    square_foot_range: str
    square_foot: str
    bedrooms: str
    bathrooms: str
    home_type: str
    heating: str
    cooling: str
    parking: str
    exterior: str
    parcel_num: str
    construction_materials: str
    roof: str
    street: str
    city: str
    state: str
    zip: str
    county: str
    amount_in_dispute: str

    def __init__(self, SHERIEF_SALE_CHILD_ID: int = None, sale: str = "", case_number: str = "", sale_type: str = "",
                 status: str = "",
                 tracts: str = "", cost_tax_bid: str = "", plaintiff: str = "",
                 attorney_for_plaintiff: str = "", defendant: str = "", property_address: str = "",
                 municipality: str = "", parcel_tax_id: str = "", comments: str = "", zillow_link: str = ""
                 , zestimate: str = "", zestibuck: str = "", events: str = "", schools: str = "", year_built: str = "",
                 lot_size: str = "", square_foot_range: str = "", square_foot: str = "", bedrooms: str = "",
                 bathrooms: str = "", home_type: str = "", heating: str = "", cooling: str = "", parking: str = "",
                 exterior: str = "", parcel_num: str = "", construction_materials: str = "", roof: str = "",
                 street: str = "", city: str = "", state: str = "", zip: str = "", county: str = "", amount_in_dispute: str = ""):
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
        self.zillow_link = zillow_link
        self.SHERIEF_SALE_CHILD_ID = SHERIEF_SALE_CHILD_ID
        self.zestimate = zestimate
        self.zestibuck = zestibuck
        self.events = events
        self.schools = schools
        self.year_built = year_built
        self.lot_size = lot_size
        self.square_foot_range = square_foot_range
        self.square_foot = square_foot
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.home_type = home_type
        self.heating = heating
        self.cooling = cooling
        self.parking = parking
        self.exterior = exterior
        self.parcel_num = parcel_num
        self.construction_materials = construction_materials
        self.roof = roof
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.county = county
        self.amount_in_dispute: str= amount_in_dispute

    def __str__(self):
        return (f"Property(sale={self.sale}, case_number={self.case_number}, sale_type={self.sale_type}, "
                f"status={self.status}, tracts={self.tracts}, cost_tax_bid={self.cost_tax_bid}, "
                f"plaintiff={self.plaintiff}, attorney_for_plaintiff={self.attorney_for_plaintiff}, "
                f"defendant={self.defendant}, property_address={self.property_address}, "
                f"municipality={self.municipality}, parcel_tax_id={self.parcel_tax_id}, comments={self.comments})")

    def convert_property_sherif_sale_alchemy(self) -> 'PropertySherifSale':
        return PropertySherifSale(sale=self.sale, case_number=self.case_number, sale_type=self.sale_type,
                                  status=self.status, tracts=self.tracts, cost_tax_bid=self.cost_tax_bid,
                                  plaintiff=self.plaintiff, attorney_for_plaintiff=self.attorney_for_plaintiff,
                                  defendant=self.defendant, property_address=self.property_address,
                                  municipality=self.municipality, parcel_tax_id=self.parcel_tax_id,
                                  comments=self.comments, SHERIEF_SALE_CHILD_ID=self.SHERIEF_SALE_CHILD_ID,
                                  zillow_link=self.zillow_link, zestimate=self.zestimate, zestibuck=self.zestibuck,
                                  events=self.events, schools=self.schools, year_built=self.year_built,
                                  lot_size=self.lot_size, square_foot_range=self.square_foot_range,
                                  square_foot=self.square_foot, bedrooms=self.bedrooms, bathrooms=self.bathrooms,
                                  home_type=self.home_type, heating=self.heating, cooling=self.cooling,
                                  parking=self.parking, exterior=self.exterior, parcel_num=self.parcel_num,
                                  construction_materials=self.construction_materials, roof=self.roof,
                                  street=self.street, city=self.city, state=self.state, zip=self.zip,
                                  county=self.county, amount_in_dispute=self.amount_in_dispute)

    def add_zillow_data(self, zillow_data: ZillowModel) -> None:
        self.zestimate = zillow_data.zestimate
        self.zestibuck = zillow_data.zestibuck
        self.events = zillow_data.get_events_as_string()
        self.schools = zillow_data.get_schools_as_string()
        self.year_built = zillow_data.yrblt
        self.lot_size = zillow_data.lot_size
        self.square_foot_range = zillow_data.sqftrange
        self.square_foot = zillow_data.sqft
        self.bedrooms = zillow_data.bedrooms
        self.bathrooms = zillow_data.bathrooms
        self.home_type = zillow_data.homeType
        self.heating = zillow_data.heating
        self.cooling = zillow_data.cooling
        self.parking = zillow_data.parking
        self.exterior = zillow_data.exterior
        self.parcel_num = zillow_data.parcel_num
        self.construction_materials = zillow_data.construction_materials
        self.roof = zillow_data.roof
        self.street = zillow_data.street
        self.city = zillow_data.city
        self.state = zillow_data.state
        self.zip = zillow_data.zip
        self.county = zillow_data.county


class PropertySherifSale(Base):
    __tablename__ = 'SHERIEF_SALE_PROPERTY_TABLE'

    id: int = Column(Numeric, primary_key=True, nullable=False, autoincrement=True)
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
    SHERIEF_SALE_CHILD_ID: int = Column(Numeric,ForeignKey('SHERIEF_SALE_CHILD_TABLE.id'), nullable=False)
    zillow_link: str = Column(String(300), nullable=True)
    # Newly added columns
    zestimate: str = Column(String(20), nullable=True)
    zestibuck: str = Column(String(50), nullable=True)
    events: str = Column(Text, nullable=True)
    schools: str = Column(Text, nullable=True)
    year_built: str = Column(String(50), nullable=True)
    lot_size: str = Column(String(80), nullable=True)
    square_foot_range: str = Column(String(80), nullable=True)
    square_foot: str = Column(String(80), nullable=True)
    bedrooms: str = Column(String(5), nullable=True)
    bathrooms: str = Column(String(5), nullable=True)
    home_type: str = Column(String(80), nullable=True)
    heating: str = Column(String(100), nullable=True)
    cooling: str = Column(String(100), nullable=True)
    parking: str = Column(String(100), nullable=True)
    exterior: str = Column(String(100), nullable=True)
    parcel_num: str = Column(String(200), nullable=True)
    construction_materials: str = Column(String(300), nullable=True)
    roof: str = Column(String(300), nullable=True)
    street: str = Column(String(300), nullable=True)
    city: str = Column(String(300), nullable=True)
    state: str = Column(String(300), nullable=True)
    zip: str = Column(String(300), nullable=True)
    county: str = Column(String(300), nullable=True)
    amount_in_dispute: str = Column(String(50), nullable=True)

    # Many-to-one relationship with SherifSale
    sherif_sale_child = relationship("SherifSaleChild", back_populates="sherif_sale_properties")

    def to_dict(self):
        """
        Serializes the PropertySherifSale object into a dictionary.
        """
        return {
            "id": self.id,
            "sale": self.sale,
            "case_number": self.case_number,
            "sale_type": self.sale_type,
            "status": self.status,
            "tracts": self.tracts,
            "cost_tax_bid": self.cost_tax_bid,
            "plaintiff": self.plaintiff,
            "attorney_for_plaintiff": self.attorney_for_plaintiff,
            "defendant": self.defendant,
            "property_address": self.property_address,
            "municipality": self.municipality,
            "parcel_tax_id": self.parcel_tax_id,
            "comments": self.comments,
            "created_at": self._serialize_date(self.created_at),
            "created_by": self.created_by,
            "SHERIEF_SALE_CHILD_ID": self.SHERIEF_SALE_CHILD_ID,
            "zillow_link": self.zillow_link,
            "zestimate": self.zestimate,
            "zestibuck": self.zestibuck,
            "events": self.events,
            "schools": self.schools,
            "year_built": self.year_built,
            "lot_size": self.lot_size,
            "square_foot_range": self.square_foot_range,
            "square_foot": self.square_foot,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "home_type": self.home_type,
            "heating": self.heating,
            "cooling": self.cooling,
            "parking": self.parking,
            "exterior": self.exterior,
            "parcel_num": self.parcel_num,
            "construction_materials": self.construction_materials,
            "roof": self.roof,
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "county": self.county,
            "amount_in_dispute": self.amount_in_dispute

        }
    @staticmethod
    def _serialize_date(value):
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return value
    def add_zillow_data(self, zillow_data: ZillowModel) -> None:
        self.zestimate = zillow_data.zestimate
        self.zestibuck = zillow_data.zestibuck
        self.events = zillow_data.get_events_as_string()
        self.schools = zillow_data.get_schools_as_string()
        self.year_built = zillow_data.yrblt
        self.lot_size = zillow_data.lot_size
        self.square_foot_range = zillow_data.sqftrange
        self.square_foot = zillow_data.sqft
        self.bedrooms = zillow_data.bedrooms
        self.bathrooms = zillow_data.bathrooms
        self.home_type = zillow_data.homeType
        self.heating = zillow_data.heating
        self.cooling = zillow_data.cooling
        self.parking = zillow_data.parking
        self.exterior = zillow_data.exterior
        self.parcel_num = zillow_data.parcel_num
        self.construction_materials = zillow_data.construction_materials
        self.roof = zillow_data.roof
        self.street = zillow_data.street
        self.city = zillow_data.city
        self.state = zillow_data.state
        self.zip = zillow_data.zip
        self.county = zillow_data.county

    def __str__(self):
        return (f"PropertySherifSale(id={self.id}, sale='{self.sale}', case_number='{self.case_number}', "
                f"property_address='{self.property_address}', status='{self.status}', "
                f"tracts='{self.tracts}', cost_tax_bid='{self.cost_tax_bid}', plaintiff='{self.plaintiff}', "
                f"attorney_for_plaintiff='{self.attorney_for_plaintiff}', defendant='{self.defendant}', "
                f"municipality='{self.municipality}', parcel_tax_id='{self.parcel_tax_id}', comments='{self.comments}', "
                f"created_at='{self.created_at}', created_by='{self.created_by}', SHERIEF_SALE_CHILD_ID='{self.SHERIEF_SALE_CHILD_ID}', "
                f"zillow_link='{self.zillow_link}', zestimate='{self.zestimate}', zestibuck='{self.zestibuck}', "
                f"events='{self.events}', schools='{self.schools}', year_built='{self.year_built}', "
                f"lot_size='{self.lot_size}', square_foot_range='{self.square_foot_range}', "
                f"bedrooms='{self.bedrooms}', bathrooms='{self.bathrooms}', "
                f"square_foot='{self.square_foot}', home_type='{self.home_type}')")

    @staticmethod
    def save_sherif_sale_to_db(property: Union[Property, 'PropertySherifSale']) -> int:
        try:
            if isinstance(property, PropertySherifSale):
                session.add(property)
                session.commit()

                print("[+] Sherif Sale saved to db 'PropertySherifSale'")
                return property.id
            else:
                # Convert and add each Property to the session
                property_sherif_sale = property.convert_property_sherif_sale_alchemy()
                session.add(property_sherif_sale)
                session.commit()
                print("[+] Sherif Sale saved to db 'Property'")
                return property_sherif_sale.id
        except Exception as e:
            session.rollback()
            print(f'Error committing to the db: {e}')
            raise e

    @staticmethod
    def save_all_sherif_sales_to_db(properties: List[Union[Property, 'PropertySherifSale']]) -> None:
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

    @staticmethod
    def get_all_where_zillow_data_is_missing(count: str, sale_type: str) -> List['PropertySherifSale']:
        try:
            properties = session.query(PropertySherifSale).filter(
                PropertySherifSale.tracts == count,
                PropertySherifSale.street == "",  # Check where street is NULL
                PropertySherifSale.state == "",  # Check where street is NULL
                PropertySherifSale.property_address != "",
                (PropertySherifSale.zillow_link != None) | (PropertySherifSale.zillow_link != ""),
                PropertySherifSale.sale_type == sale_type,
                PropertySherifSale.created_at >= datetime(2024, 9, 10)

            ).all()
            return properties
        except Exception as e:
            print(f'Error fetching properties: {e}')
            raise e

    @staticmethod
    def get_all_where_ammount_in_dispute_is_missing( sale_type: str) -> List['PropertySherifSale']:
        try:
            properties = session.query(PropertySherifSale).filter(
                (PropertySherifSale.amount_in_dispute.is_(None)) | (PropertySherifSale.amount_in_dispute != ""),
                PropertySherifSale.sale_type == sale_type,
                PropertySherifSale.created_at >= datetime(2024, 9, 10)

            ).all()
            return properties
        except Exception as e:
            print(f'Error fetching properties: {e}')
            raise e

    @staticmethod
    def update_zillow_data_in_duplicates():
        try:
            # Define the query
            query = """
            UPDATE SHERIEF_SALE_PROPERTY_TABLE t1
            JOIN (
                -- Subquery to find duplicate case_number and get Zillow data from one of them
                SELECT t1.id AS id_with_data, t2.id AS id_without_data,
                       t1.ZILLOW_LINK, t1.ZESTIMATE, t1.ZESTIBUCK, t1.SQUARE_FOOT, t1.BEDROOMS, t1.BATHROOMS,
                       t1.HOME_TYPE, t1.HEATING, t1.COOLING, t1.PARKING, t1.EXTERIOR, t1.CONSTRUCTION_MATERIALS, t1.ROOF,
                       t1.STREET, t1.CITY, t1.STATE, t1.ZIP, t1.COUNTY
                FROM SHERIEF_SALE_PROPERTY_TABLE t1
                JOIN SHERIEF_SALE_PROPERTY_TABLE t2
                    ON t1.case_number = t2.case_number
                    AND t1.id != t2.id
                -- Ensure t1 has Zillow data
                WHERE (t1.ZILLOW_LINK IS NOT NULL OR t1.STATE IS NOT NULL OR t1.ZIP IS NOT NULL)
                -- Ensure t2 does not have Zillow data
                AND (t2.ZILLOW_LINK IS NULL OR t2.ZESTIMATE IS NULL OR t2.ZESTIBUCK IS NULL)
            ) AS t2
            -- Update the records without Zillow data
            ON t1.id = t2.id_without_data
            SET 
                t1.ZILLOW_LINK = t2.ZILLOW_LINK,
                t1.ZESTIMATE = t2.ZESTIMATE,
                t1.ZESTIBUCK = t2.ZESTIBUCK,
                t1.SQUARE_FOOT = t2.SQUARE_FOOT,
                t1.BEDROOMS = t2.BEDROOMS,
                t1.BATHROOMS = t2.BATHROOMS,
                t1.HOME_TYPE = t2.HOME_TYPE,
                t1.HEATING = t2.HEATING,
                t1.COOLING = t2.COOLING,
                t1.PARKING = t2.PARKING,
                t1.EXTERIOR = t2.EXTERIOR,
                t1.CONSTRUCTION_MATERIALS = t2.CONSTRUCTION_MATERIALS,
                t1.ROOF = t2.ROOF,
                t1.STREET = t2.STREET,
                t1.CITY = t2.CITY,
                t1.STATE = t2.STATE,
                t1.ZIP = t2.ZIP,
                t1.COUNTY = t2.COUNTY;
            """

            # Execute the query
            session.execute(text(query))
            session.commit()  # Commit the changes
            print("Zillow data updated in duplicate records.")

        except Exception as e:
            session.rollback()  # Rollback in case of error
            print(f"An error occurred: {e}")

        finally:
            session.close()  # Close the session