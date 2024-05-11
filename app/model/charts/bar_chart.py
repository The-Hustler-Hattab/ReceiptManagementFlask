from collections import defaultdict
from typing import List, Dict

from app.util.data_manipulation import DataManipulation


class DataChartModel:
    vendor: str
    color: str
    data: List[float]

    def __init__(self, vendor: str):
        self.vendor = vendor
        self.color = DataManipulation.get_color(vendor)
        self.data = []

    def __str__(self) -> str:
        return f'vendor: {self.vendor}, data: {self.data}, color: {self.color}'

    def to_dict(self) -> dict:
        return {
            "vendor": self.vendor,
            "color": self.color,
            "data": self.data
        }


class BarChart:
    """
    Represents data for analytics chart.

    Attributes:
        vendor (str): The vendor name.
        month (int): The month.
        year (int): The year.
        total_amount (float): The total amount.
        total_amount_month (float): The total amount for the month.
        total_amount_subtotal (float): The total amount subtotal.
        total_amount_subtotal_month (float): The total amount subtotal for the month.
        total_tax (float): The total tax.
        total_tax_month (float): The total tax for the month.
    """
    vendor: str
    month: int
    year: int
    total_amount: float
    total_amount_month: float
    total_amount_subtotal: float
    total_amount_subtotal_month: float
    total_tax: float
    total_tax_month: float

    @classmethod
    def empty(cls):
        """Creates an empty AnalyticsChart object."""
        return cls("", 0, 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0)

    def __init__(self, vendor: str, month: int, year: int, total_amount: float, total_amount_month: float,
                 total_amount_subtotal: float, total_amount_subtotal_month: float, total_tax: float,
                 total_tax_month: float) -> None:
        self.vendor = vendor
        self.month = month
        self.year = year
        self.total_amount = total_amount
        self.total_amount_month = total_amount_month
        self.total_amount_subtotal = total_amount_subtotal
        self.total_amount_subtotal_month = total_amount_subtotal_month
        self.total_tax = total_tax
        self.total_tax_month = total_tax_month

    def __str__(self) -> str:
        return (
            f'vendor: {self.vendor}, month: {self.month}, year: {self.year}, total_amount: {self.total_amount}, '
            f'total_amount_month: {self.total_amount_month}, total_amount_subtotal: {self.total_amount_subtotal}, '
            f'total_amount_subtotal_month: {self.total_amount_subtotal_month}, total_tax: {self.total_tax}, total_tax_month: {self.total_tax_month}')

    @staticmethod
    def get_labels(chart_models: List['BarChart'], field_name: str) -> List[str]:
        """
          Retrieves labels for the given field name from a list of AnalyticsChart objects.

          Args:
              chart_models (List['AnalyticsChart']): A list of AnalyticsChart objects.
              field_name (str): The field name for which to retrieve labels.

          Returns:
              List[str]: A list of labels.
          """
        labels_set = set()
        for chart in chart_models:
            field_value = getattr(chart, field_name)
            if field_value != 0.0:
                labels_set.add(f'{chart.year}-{chart.month}: ${field_value}')

        labels_list = list(labels_set)
        labels_list.sort()
        return labels_list

    @staticmethod
    def get_data_all(chart_models: List['BarChart']) -> Dict[str, Dict]:
        """
        Retrieves all data for the given list of AnalyticsChart objects.

        Args:
            chart_models (List['AnalyticsChart']): A list of AnalyticsChart objects.

        Returns:
            Dict[str, Dict]: A dictionary containing data for different fields.
        """
        data_chart_model_dict: Dict[str, Dict] = {}
        data_chart_model_dict['total_amount'] = {  "data": BarChart.get_data(chart_models, 'total_amount'),
                                                   "label": BarChart.get_labels(chart_models, 'total_amount_month')}

        data_chart_model_dict['total_amount_subtotal'] = {  "data": BarChart.get_data(chart_models, 'total_amount_subtotal'),
                                                   "label": BarChart.get_labels(chart_models, 'total_amount_subtotal_month')}

        data_chart_model_dict['total_tax'] = {  "data": BarChart.get_data(chart_models, 'total_tax'),
                                                   "label": BarChart.get_labels(chart_models, 'total_tax_month')}


        return data_chart_model_dict

    @staticmethod
    def get_data(chart_models: List['BarChart'], field_name: str) -> List[dict]:
        """
         Retrieves data for the given field name from a list of AnalyticsChart objects.

         Args:
             chart_models (List['AnalyticsChart']): A list of AnalyticsChart objects.
             field_name (str): The field name for which to retrieve data.

         Returns:
             List[dict]: A list of data.
         """
        data_chart_models = []
        vendors: list[str] = BarChart.get_list_of_vendors_ordered_non_duplicate(chart_models)
        for vendor in vendors:
            data_chart_models.append(BarChart.get_data_for_vendor(vendor, chart_models, field_name))

        return data_chart_models

    @staticmethod
    def get_data_for_vendor(vendor: str, chart_models: List['BarChart'], field_name: str) -> dict:
        """
        Retrieves data for a specific vendor and field name from a list of AnalyticsChart objects.

        Args:
            vendor (str): The vendor name.
            chart_models (List['AnalyticsChart']): A list of AnalyticsChart objects.
            field_name (str): The field name for which to retrieve data.

        Returns:
            dict: Data for the vendor and field name.
        """
        data_chart_models: DataChartModel = DataChartModel(vendor)

        for chart in chart_models:
            if chart.vendor == vendor:
                field_value = getattr(chart, field_name)
                data_chart_models.data.append(field_value)
        return data_chart_models.to_dict()

    @staticmethod
    def get_list_of_vendors_ordered_non_duplicate(chart_models: list['BarChart']) -> list:
        """
               Retrieves a list of vendors ordered non-duplicated from a list of AnalyticsChart objects.

               Args:
                   chart_models (list['AnalyticsChart']): A list of AnalyticsChart objects.

               Returns:
                   list: A list of vendors.
               """
        months_set = set()
        for e in chart_models:
            months_set.add(e.vendor)

        months: list = list(months_set)
        months.sort()
        return months

    @staticmethod
    def filter_non_zero_total_amount(chart_models: List['BarChart']) -> List['BarChart']:
        """
        Filters out AnalyticsChart objects with zero total amount.

        Args:
            chart_models (List['AnalyticsChart']): A list of AnalyticsChart objects.

        Returns:
            List['AnalyticsChart']: A list of filtered AnalyticsChart objects.
        """
        # Group objects by month and year
        grouped_data = defaultdict(list)
        for chart_model in chart_models:
            grouped_data[(chart_model.month, chart_model.year)].append(chart_model)

        # Filter out entries with all vendors having zero total amount for a specific month and year
        filtered_charts = []
        for month_year, entries in grouped_data.items():
            total_amounts = [entry.total_amount for entry in entries]
            if all(amount == 0.0 for amount in total_amounts):
                continue
            else:
                filtered_charts.extend(entries)

        return filtered_charts
