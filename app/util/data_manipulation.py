

class DataManipulation:
    @staticmethod
    def convert_keywords(vendor_name: str, mappings: dict) -> str:
        for keyword, replacement in mappings.items():
            if keyword.lower() in vendor_name.lower():
                vendor_name = replacement
                break  # Exit loop after the first match to ensure only one replacement is made
        return vendor_name

    # Example mappings
    mappings = {
        "homedepo": "HOME DEPOT",
        "lowe": "LOWES",
        "walmart": "WALMART",

    }