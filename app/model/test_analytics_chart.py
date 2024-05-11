from unittest import TestCase

from app.model.analytics_chart import AnalyticsChart
from app.util.data_manipulation import DataManipulation


class TestDataManipulation(TestCase):

    def test_get_list_of_months_ordered_non_duplicate(self):
        chart1 = AnalyticsChart.empty()
        chart1.month = 1
        chart1.year = 2024
        chart1.total_amount_month=154163.0
        chart2 = AnalyticsChart.empty()
        chart2.month = 2
        chart2.year = 2024
        chart2.total_amount_month=154163.0

        chart3 = AnalyticsChart.empty()
        chart3.month = 2
        chart3.year = 2024
        chart3.total_amount_month=154163.0

        chart4 = AnalyticsChart.empty()
        chart4.month = 3
        chart4.year = 2024
        chart4.total_amount_month=154163.0

        chart5 = AnalyticsChart.empty()
        chart5.month = 1
        chart5.year = 2024
        chart5.total_amount_month=154163.0

        chart6 = AnalyticsChart.empty()
        chart6.month = 5
        chart6.year = 2024
        chart6.total_amount_month=154163.0

        chart7 = AnalyticsChart.empty()
        chart7.month = 2
        chart7.year = 2024
        chart7.total_amount_month=154163.0

        chart8 = AnalyticsChart.empty()
        chart8.month = 6
        chart8.year = 2021
        chart8.total_amount_month=154163.0

        chart9 = AnalyticsChart.empty()
        chart9.month = 3
        chart9.year = 2020
        chart9.total_amount_month=154163.0

        print(chart1)
        charts: list[AnalyticsChart] = [chart1, chart2, chart3, chart4, chart5, chart6, chart7, chart8, chart9]
        months = AnalyticsChart.get_labels(charts,"total_amount_month")
        print(months)

    def test_get_list_of_vendors_ordered_non_duplicate(self):
        chart1 = AnalyticsChart.empty()
        chart1.vendor = "wal-mart"
        chart2 = AnalyticsChart.empty()
        chart2.vendor = "wal-mart"
        chart3 = AnalyticsChart.empty()
        chart3.vendor = "lowes"

        chart4 = AnalyticsChart.empty()
        chart4.vendor = "home depot"

        chart5 = AnalyticsChart.empty()
        chart5.vendor = "wal-mart"

        chart6 = AnalyticsChart.empty()
        chart6.vendor = "kraft"

        chart7 = AnalyticsChart.empty()
        chart7.vendor = "giant eagle"

        chart8 = AnalyticsChart.empty()
        chart8.vendor = "wal-mart"

        chart9 = AnalyticsChart.empty()
        chart9.vendor = "lowes"

        print(chart1)
        charts: list[AnalyticsChart] = [chart1, chart2, chart3, chart4, chart5, chart6, chart7, chart8, chart9]
        months = AnalyticsChart.get_list_of_vendors_ordered_non_duplicate(charts)
        print(months)
        self.assertListEqual(["giant eagle", "home depot", "kraft", "lowes", "wal-mart"], months)


