from typing import List, Dict

from app.util.data_manipulation import DataManipulation


class PieChart:
    vendor: str
    total_amount: float
    total_amount_subtotal: float
    total_tax: float

    def __init__(self, vendor: str, total_amount: float, total_amount_subtotal: float, total_tax: float) -> None:
        self.vendor = vendor
        self.total_amount = total_amount
        self.total_amount_subtotal = total_amount_subtotal
        self.total_tax = total_tax

    def __str__(self) -> str:
        return f'vendor: {self.vendor}, total_amount: {self.total_amount}, total_amount_subtotal: {self.total_amount_subtotal}, total_tax: {self.total_tax}'

    @staticmethod
    def get_by_field(charts: List['PieChart'], category: str) -> List[str]:
        chart_list = []
        for chart in charts:
            field_value = getattr(chart, category)
            chart_list.append(field_value)

        return chart_list

    @staticmethod
    def get_background_colors(charts: List['PieChart']) -> List[str]:
        background_colors = []
        for chart in charts:
            background_colors.append(DataManipulation.get_color(chart.vendor))
        return background_colors

    @staticmethod
    def get_hover_colors(charts: List['PieChart']) -> List[str]:
        background_colors = []
        for chart in charts:
            background_colors.append(DataManipulation.get_hover_color(chart.vendor))
        return background_colors

    @staticmethod
    def get_data_all(chart_models: List['PieChart']) -> Dict[str, Dict]:
        labels = PieChart.get_by_field(chart_models, 'vendor')
        background_colors = PieChart.get_background_colors(chart_models)
        hover_colors = PieChart.get_hover_colors(chart_models)
        data_chart_model_dict: Dict[str, Dict] = {}
        data_chart_model_dict['total_amount'] = {"data": PieChart.get_by_field(chart_models, 'total_amount'),
                                                 "label": labels, "backgroundColor": background_colors,
                                                 "hoverBackgroundColor": hover_colors}

        data_chart_model_dict['total_amount_subtotal'] = {
            "data": PieChart.get_by_field(chart_models, 'total_amount_subtotal'),
            "label": labels, "backgroundColor": background_colors, "hoverBackgroundColor": hover_colors}

        data_chart_model_dict['total_tax'] = {"data": PieChart.get_by_field(chart_models, 'total_tax'),
                                              "label": labels, "backgroundColor": background_colors,
                                              "hoverBackgroundColor": hover_colors}

        return data_chart_model_dict
