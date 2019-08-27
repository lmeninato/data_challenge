import unittest
from src.read_data import *
from collections import OrderedDict


class RowMergeTestCase(unittest.TestCase):
    def setUp(self):
        self.test_results = read_csv_lines(path="test_1/input/Border_Crossing_Entry_Data.csv")

    def test_is_ordered_dict(self):
        self.assertIsInstance(self.test_results, OrderedDict)
    # add more test cases


if __name__ == "__main__":
    unittest.main(verbosity=2)
