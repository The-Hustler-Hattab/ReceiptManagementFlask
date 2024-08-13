from datetime import datetime


class DateUtil:
    @staticmethod
    def convert_string_to_date(date_str: str) -> datetime:
        """
        Convert a string to a date object using the format YYYY-MM-DD
        :param date_str: The date string to convert
        :return: The date object
        """
        return datetime.strptime(date_str, "%Y-%m-%d")