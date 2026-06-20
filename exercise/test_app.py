import unittest
import unittest.mock
from unittest import mock

import app


class TestAdd(unittest.TestCase):
    num = 5

    def test_add_number(self):
        self.assertEqual(app.add(2, 3), self.num)

    def test_add_number_2(self):
        self.assertEqual(app.add(2.0, -3), -1)


class TestCircle(unittest.TestCase):
    __PI: float = 3.142

    def setUp(self):
        self.circ: app.Circle = app.Circle(4.0)

    def test_circle_area(self):
        self.assertEqual(self.circ.area(), 804.35)

    # Replace app.get_data with a fake version for testing
    @mock.patch("app.get_data", return_value={"value": 6})
    def test_process_data(self, mock_get):
        result = app.process_data()
        self.assertEqual(result, 12)
        mock_get.assert_called_once()

