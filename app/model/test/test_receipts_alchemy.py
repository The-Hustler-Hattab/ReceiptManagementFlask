from datetime import datetime
from typing import List, Dict
from unittest import TestCase

from app.model.charts.bar_chart import BarChart, DataChartModel
from app.model.db.receipts_alchemy import Receipts


class TestReceipts(TestCase):

    def test_delete_by_file_path(self):
        Receipts.delete_by_file_path("")

    def test_fetch_between_chart_model(self):
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        results = Receipts.fetch_between_bar_chart_model_non_null_vendors(start_date, end_date)
        for chart in results:
            print(chart)

    def test_fetch_between_chart_model_include_null_vendors(self):
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        results = Receipts.fetch_between_chart_model_include_null_vendors(start_date, end_date)
        for chart in results:
            print(chart)

        print("Total: ", len(results))
        charts = BarChart.filter_non_zero_total_amount(results)
        for chart in charts:
            print(chart)
        print("Total: ", len(charts))

        data: List[DataChartModel] = BarChart.get_data(charts, "total_amount_month")
        for chart in data:
            print(chart)
        print("Total: ", len(data))

        data_all: Dict[str, dict] = BarChart.get_data_all(charts)

        for key, value in data_all.items():
            print(key)
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}:")
                for item in sub_value:
                    print(f"        {item}")

    def test_fetch_between_pie_chart_model(self):
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        results = Receipts.fetch_between_pie_chart_model(start_date, end_date)
        for chart in results:
            print(chart)


    def test_fetch_between_line_chart_model(self):
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        results = Receipts.fetch_between_line_chart_model(start_date, end_date)
        for chart in results:
            print(chart)