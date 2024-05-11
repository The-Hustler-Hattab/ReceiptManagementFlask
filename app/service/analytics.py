from datetime import date

from flask import Response, jsonify

from app.model.charts.bar_chart import BarChart
from app.model.charts.horizantal_chart import HorizontalChart
from app.model.charts.line_chart import LineChart
from app.model.charts.pie_chart import PieChart
from app.model.db.receipts_alchemy import Receipts


class AnalyticsService:

    @staticmethod
    def get_bar_chart_data(start_date: date, end_date: date) -> tuple[Response, int]:
        analytics_charts: list[BarChart] = (Receipts.
                                            fetch_between_bar_chart_model_non_null_vendors(start_date, end_date))
        charts_filtered = BarChart.filter_non_zero_total_amount(analytics_charts)

        data_all: dict[str, dict] = BarChart.get_data_all(charts_filtered)

        return jsonify({'message': 'fetched data successfully', 'data_all': data_all}), 200

    @staticmethod
    def get_pie_chart_data(start_date: date, end_date: date) -> tuple[Response, int]:
        analytics_charts: list[PieChart] = (Receipts.
                                            fetch_between_pie_chart_model(start_date, end_date))

        data_all: dict[str, dict] = PieChart.get_data_all(analytics_charts)

        return jsonify({'message': 'fetched data successfully', 'data_all': data_all}), 200

    @staticmethod
    def get_line_chart_data(start_date: date, end_date: date) -> tuple[Response, int]:
        analytics_charts: list[LineChart] = (Receipts.
                                             fetch_between_line_chart_model(start_date, end_date))

        data_all: dict[str, dict] = LineChart.get_data_all(analytics_charts)

        return jsonify({'message': 'fetched data successfully', 'data_all': data_all}), 200

    @staticmethod
    def get_horizontal_chart_data(start_date: date, end_date: date) -> tuple[Response, int]:
        analytics_charts: list[HorizontalChart] = (Receipts.
                                             fetch_between_horizontal_chart_model(start_date, end_date))

        data_all: dict[str, dict] = HorizontalChart.get_data_all(analytics_charts)

        return jsonify({'message': 'fetched data successfully', 'data_all': data_all}), 200
