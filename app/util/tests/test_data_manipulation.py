from unittest import TestCase

from app.util.data_manipulation import DataManipulation


class TestDataManipulation(TestCase):

    def test_map_to_month(self):
        month_list = DataManipulation.map_to_month([1, 2, 3, 5, 6])
        print(month_list)
        self.assertListEqual(["January", "February", "March", "May", "June"], month_list)
