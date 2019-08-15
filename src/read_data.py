import csv
from datetime import datetime


def process_row(data_row):
    date = format_date(data_row['Date'])
    border = data_row['border']
    return date, border


def format_date(date):
    return datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')


if __name__ == '__main__':
    results = {}
    with open("insight_testsuite/tests/test_1/input/Border_Crossing_Entry_Data.csv") as f:
        data = csv.DictReader(f)
        for row in data:
            process_row(row)
