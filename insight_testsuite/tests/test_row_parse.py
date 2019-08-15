import unittest
from src.read_data import *


def read_in_entire_file(path="insight_testsuite/tests/test_1/input/Border_Crossing_Entry_Data.csv",
                        process_test_row=False):
    """
    Used to quickly load an entire file into memory. For testing and development.
    :param path: path to input csv
    :param process_test_row: process test_row or not
    :return: list of OrderDict rows
    """
    all_rows = []
    with open(path) as file:
        test_data = csv.DictReader(file)
        for test_count, test_row in enumerate(test_data):
            if process_test_row:
                all_rows.append(process_row(test_count, test_row))
            else:
                all_rows.append(test_row)
    return all_rows


class RowParserTestCase(unittest.TestCase):
    def setUp(self):
        self.all_rows = read_in_entire_file(path="test_1/input/Border_Crossing_Entry_Data.csv")
        self.processed_rows = read_in_entire_file(path="test_1/input/Border_Crossing_Entry_Data.csv",
                                                  process_test_row=True)

    def test_parse_str_border(self):
        border = parse_field(parse_str_field, 0, self.all_rows[0], 'Border')
        self.assertEqual(border, 'US-Canada Border')

    def test_parse_str_measure(self):
        measure = parse_field(parse_str_field, 0, self.all_rows[0], 'Measure')
        self.assertEqual(measure, 'Truck Containers Full')

    def test_parse_date(self):
        date = parse_field(parse_date, 0, self.all_rows[0], 'Date')
        self.assertIsInstance(date, datetime)

    def test_parse_date_year(self):
        date = parse_field(parse_date, 0, self.all_rows[0], 'Date')
        self.assertEqual(date.year, 2019)

    def test_parse_int_value(self):
        value = parse_field(parse_int_field, 0, self.all_rows[0], 'Value')
        self.assertEqual(value, 6483)

    def test_process_row(self):
        self.assertEqual(self.processed_rows[0]['Month'], 3)

    def test_bad_input(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)

