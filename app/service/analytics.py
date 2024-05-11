from datetime import date

from flask import Response, jsonify

from app.model.analytics_chart import AnalyticsChart
from app.model.receipts_alchemy import Receipts


class AnalyticsService:

    @staticmethod
    def get_bar_chart_data(start_date: date, end_date: date) -> tuple[Response, int]:
        analytics_charts: list[AnalyticsChart] = (Receipts.
                                                  fetch_between_chart_model_non_null_vendors(start_date, end_date))
        charts_filtered = AnalyticsChart.filter_non_zero_total_amount(analytics_charts)

        data_all: dict[str, dict] = AnalyticsChart.get_data_all(charts_filtered)

        return jsonify({'message': 'fetched data successfully', 'data_all': data_all}), 200
