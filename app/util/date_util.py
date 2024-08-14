from datetime import datetime
from typing import Optional


class DateUtil:
    @staticmethod
    def convert_string_to_date(date_str: str) -> datetime:
        """
        Convert a string to a date object using the format YYYY-MM-DD
        :param date_str: The date string to convert
        :return: The date object
        """
        return datetime.strptime(date_str, "%Y-%m-%d")

    @staticmethod
    def prepend_timestamp_to_filename(filename: str, timestamp_format: Optional[str] = "%Y%m%d_%H%M%S") -> str:
        """
        Prepends the current timestamp to the given filename.

        Args:
            filename (str): The filename to which the timestamp will be prepended.
            timestamp_format (Optional[str]): The format in which the timestamp should be displayed.
                                              Defaults to "%Y%m%d_%H%M%S".

        Returns:
            str: The filename with the prepended timestamp.
        """
        current_timestamp = datetime.now().strftime(timestamp_format)
        return f"{current_timestamp}_{filename}"
