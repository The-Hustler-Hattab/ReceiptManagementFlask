from typing import List, Dict

from app.util.data_manipulation import DataManipulation


class HorizontalChart:
    year: int
    month: int
    total_cost: float
    total_sub_total: float
    total_tax: float

    def __init__(self, year: int, month: int, total_cost: float, total_sub_total: float, total_tax: float) -> None:
        self.year = year
        self.month = month
        self.total_cost = total_cost
        self.total_sub_total = total_sub_total
        self.total_tax = total_tax

    def __str__(self) -> str:
        return f'year: {self.year}, month: {self.month}, total_cost: {self.total_cost}, total_sub_total: {self.total_sub_total}, total_tax: {self.total_tax}'

    @staticmethod
    def get_by_field(charts: List['HorizontalChart'], category: str) -> List[str]:
        chart_list = []
        for chart in charts:
            field_value = getattr(chart, category)
            chart_list.append(field_value)

        return chart_list

    @staticmethod
    def get_labels(charts: List['HorizontalChart']) -> List[str]:
        chart_list = []
        for chart in charts:
            chart_list.append(f'{DataManipulation.map_to_month(chart.month)}-{chart.year}')
        return chart_list


    @staticmethod
    def get_data_all(chart_models: List['HorizontalChart']) -> Dict[str, Dict]:
        labels = HorizontalChart.get_labels(chart_models)

        data_chart_model_dict: Dict[str, Dict] = {}
        data_chart_model_dict['total_amount'] = {"data": HorizontalChart.get_by_field(chart_models, 'total_cost'),
                                                 "label": labels, "borderColor": '--red-500'}

        data_chart_model_dict['total_amount_subtotal'] = {
            "data": HorizontalChart.get_by_field(chart_models, 'total_sub_total'),
            "label": labels, "borderColor": '--blue-500'}

        data_chart_model_dict['total_tax'] = {"data": HorizontalChart.get_by_field(chart_models, 'total_tax'),
                                              "label": labels, "borderColor": '--pink-500'}

        return data_chart_model_dict
