
import json

class SheriffSaleDetailModel:

    file_path: str
    sheriff_sale_child_id: int

    def __init__(self, file_path: str, sheriff_sale_child_id: int):
        self.file_path = file_path
        self.sheriff_sale_child_id = sheriff_sale_child_id

    def __str__(self):
        return f"SheriffSaleDetailModel(file_path='{self.file_path}', sheriff_sale_child_id={self.sheriff_sale_child_id})"

    def to_dict(self):
        # Convert the object's attributes to a dictionary
        return {
            'file_path': self.file_path,
            'sheriff_sale_child_id': self.sheriff_sale_child_id
        }

    def to_json(self):
        # Convert the dictionary representation to a JSON string
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str):
        # Parse the JSON string into a dictionary
        data = json.loads(json_str)
        # Create a new instance of the class using the parsed data
        return cls(**data)
