import unittest
from src.read_data import read_csv_lines, merge_row
from collections import OrderedDict


class RowMergeTestCase(unittest.TestCase):
    def setUp(self):
        self.merged_rows = read_csv_lines(path="../insight_testsuite/tests/test_1/input/"
                                               "Border_Crossing_Entry_Data.csv")
        self.new_tuple = (2020, 1, 'New Border', 'New Measure')
        self.new_value = 1
        self.merged_rows[self.new_tuple] = self.new_value

    def test_is_ordered_dict(self):
        self.assertIsInstance(self.merged_rows, OrderedDict)

    def test_get_key(self):
        sample_tuple = (2019, 3, 'US-Mexico Border', 'Pedestrians')
        row_value = 346158
        self.assertEqual(self.merged_rows[sample_tuple], row_value)

    def test_add_new_row(self):
        self.assertEqual(self.merged_rows[self.new_tuple], self.new_value)

    def test_add_existing_row(self):
        count = -1  # just used for logging errors
        row = OrderedDict([('Port Name', 'a port'),
                           ('State', 'a state'),
                           ('Port Code', 'a port code'),
                           ('Border', 'New Border'),
                           ('Date', '01/01/2020 12:00:00 AM'),
                           ('Measure', 'New Measure'),
                           ('Value', 1),
                           ('Location', 'POINT (-115.48433000000001 32.67524)')])

        new_merged_rows = merge_row(self.merged_rows, count, row)
        self.assertEqual(new_merged_rows[self.new_tuple], 2)

    # test adding bad inputs


if __name__ == "__main__":
    unittest.main(verbosity=2)
