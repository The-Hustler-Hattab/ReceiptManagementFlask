import hashlib
from typing import Union, IO


class DataManipulation:
    # Example mappings
    mappings = {
        "homedepo": "HOME DEPOT",
        "lowe": "LOWES",
        "walmart": "WALMART",
        "aws": "AWS",
        "microsoft": "MICROSOFT",

    }

    @staticmethod
    def convert_keywords(vendor_name: str, mappings: dict) -> str:
        for keyword, replacement in mappings.items():
            if keyword.lower() in vendor_name.lower():
                vendor_name = replacement
                break  # Exit loop after the first match to ensure only one replacement is made
        return vendor_name

    @staticmethod
    def get_color(vendor: str) -> str:
        if vendor.upper() == "WALMART":
            return "--blue-300"
        elif vendor.upper() == "HOME DEPOT":
            return "--yellow-500"
        elif vendor.upper() == "LOWES":
            return "--blue-900"
        elif vendor.upper() == "AWS":
            return "--orange-600"
        elif vendor.upper() == "MICROSOFT":
            return "--blue-600"
        elif vendor.upper() == "Allegheny County".upper():
            return "--green-500"
        elif vendor.upper() == "LEGALZOOM".upper():
            return "--purple-500"
        elif vendor.upper() == "BusyBeaver".upper():
            return "--pink-500"
        elif vendor.upper() == "American_Home_Shield".upper():
            return "--yellow-500"
        elif vendor.upper() == "GoDaddy".upper():
            return "--pink-800"
        elif vendor.upper() == "GitHub".upper():
            return "--blue-800"
        elif vendor.upper() == "ChatGPT".upper():
            return "--blue-500"
        elif vendor.upper() == "PA Commercial PAVING".upper():
            return "--orange-900"
        elif vendor.upper() == "A1 GARAGE DOORservice".upper():
            return "--green-900"
        elif vendor.upper() == "ACEABLE AGENT".upper():
            return "--blue-300"
        elif vendor.upper() == "County of Allegheny Treasurer".upper():
            return "--yellow-300"
        else:
            return "--red-500"

    @staticmethod
    def get_hover_color(vendor: str) -> str:
        if vendor.upper() == "WALMART":
            return "--blue-200"
        elif vendor.upper() == "HOME DEPOT":
            return "--yellow-400"
        elif vendor.upper() == "LOWES":
            return "--blue-800"
        elif vendor.upper() == "AWS":
            return "--orange-500"
        elif vendor.upper() == "MICROSOFT":
            return "--blue-500"
        elif vendor.upper() == "Allegheny County".upper():
            return "--green-400"
        elif vendor.upper() == "LEGALZOOM".upper():
            return "--purple-400"
        elif vendor.upper() == "BusyBeaver".upper():
            return "--pink-400"
        elif vendor.upper() == "American_Home_Shield".upper():
            return "--yellow-400"
        elif vendor.upper() == "GoDaddy".upper():
            return "--pink-700"
        elif vendor.upper() == "GitHub".upper():
            return "--blue-700"
        elif vendor.upper() == "ChatGPT".upper():
            return "--blue-400"
        elif vendor.upper() == "PA Commercial PAVING".upper():
            return "--orange-800"
        elif vendor.upper() == "A1 GARAGE DOORservice".upper():
            return "--green-800"
        elif vendor.upper() == "ACEABLE AGENT".upper():
            return "--blue-200"
        elif vendor.upper() == "County of Allegheny Treasurer".upper():
            return "--yellow-300"
        else:
            return "--red-400"

    @staticmethod
    def map_to_month(month_numbers: int) -> str:
        month_mapping = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        return month_mapping[month_numbers]

    @staticmethod
    def compute_hash(document_file: Union[bytes, IO[bytes]]) -> str:
        # Initialize the hash object (using SHA-256 as an example)
        hash_obj = hashlib.sha256()

        if isinstance(document_file, bytes):
            # If the document is a bytes object, update the hash directly
            hash_obj.update(document_file)
        else:
            # If the document is a file-like object, read it in chunks of 1 MB
            for chunk in iter(lambda: document_file.read(1048576), b''):
                hash_obj.update(chunk)

        # Return the hexadecimal digest of the hash
        return hash_obj.hexdigest()
