import json


class ZillowModel:
    zestimate: str  # zestimate
    zestibuck: str  # zestibuck
    yrblt: str  # yrblt
    lot_size: str  # Lot size:
    sqftrange: str  # sqftrange
    sqft: str  # sqft
    bedrooms: str  # Bedrooms:
    bathrooms: str  # bathrooms:
    homeType: str  # homeType
    heating: str  # Heating features:
    cooling: str  # Cooling features:
    parking: str  # Parking features:
    exterior: str  # Exterior features:
    parcel_num: str  # Parcel number:
    construction_materials: str  # Construction materials:
    roof: str  # Roof:

    street: str  # aamgnrc1
    city: str  # city
    state: str  # state
    zip: str  # zip
    county: str  # cnty

    events: list[str]  # events
    schools: list['SchoolModel']  # schools


    def get_schools_as_string(self)->str:
        return '\n'.join([str(school) for school in self.schools])

    def get_events_as_string(self)->str:
        return '\n'.join([str(event) for event in self.events])

class SchoolModel:
    name: str
    rating: int
    level: str
    grades: str
    type: str

    def __init__(self, name, rating, level, grades, type):
        self.name = name
        self.rating = rating
        self.level = level
        self.grades = grades
        self.type = type

    # Method to convert JSON data to a list of SchoolModel objects
    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        return [cls(item['name'], item['rating'], item['level'], item['grades'], item['type']) for item in data]

    def __str__(self):
        return f"School: {self.name}, Rating: {self.rating}, Level: {self.level}, Grades: {self.grades}, Type: {self.type}"

class EventModel:
    date: str
    price: int
    pricePerSquareFoot: int
    event: str
    source: str

    def __init__(self, date: str, price: int, price_per_square_foot: int, event: str, source: str):
        self.date = date
        self.price = price
        self.pricePerSquareFoot = price_per_square_foot
        self.event = event
        self.source = source

    @classmethod
    def from_json(cls, json_data: str):
        data = json.loads(json_data)
        return [
            cls(item['date'], item['price'], item['pricePerSquareFoot'], item['event'], item['source'])
            for item in data
        ]

    def __str__(self):
        return (f"EventModel(date='{self.date}', price={self.price}, "
                f"pricePerSquareFoot={self.pricePerSquareFoot}, event='{self.event}', source='{self.source}')")
