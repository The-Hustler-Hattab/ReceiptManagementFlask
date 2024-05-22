

class DataManipulation:
    # Example mappings
    mappings = {
        "homedepo": "HOME DEPOT",
        "lowe": "LOWES",
        "walmart": "WALMART",
        "aws": "AWS",
        "azure": "AZURE",

    }
    @staticmethod
    def convert_keywords(vendor_name: str, mappings: dict) -> str:
        for keyword, replacement in mappings.items():
            if keyword.lower() in vendor_name.lower():
                vendor_name = replacement
                break  # Exit loop after the first match to ensure only one replacement is made
        return vendor_name

    @staticmethod
    def get_color(vendor:str) -> str:
        if vendor.upper() == "WALMART":
            return "--blue-400"
        elif vendor.upper() == "HOME DEPOT":
            return "--yellow-500"
        elif vendor.upper() == "LOWES":
            return "--blue-900"
        elif vendor.upper() == "AWS":
            return "--orange-600"
        elif vendor.upper() == "AZURE":
            return "--blue-800"
        else:
            return "--red-500"

    @staticmethod
    def get_hover_color(vendor: str) -> str:
        if vendor.upper() == "WALMART":
            return "--blue-300"
        elif vendor.upper() == "HOME DEPOT":
            return "--yellow-400"
        elif vendor.upper() == "LOWES":
            return "--blue-800"
        elif vendor.upper() == "AWS":
            return "--orange-500"
        elif vendor.upper() == "AZURE":
            return "--blue-700"
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