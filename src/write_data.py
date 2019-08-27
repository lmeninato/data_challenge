import csv
from src.read_data import get_monthly_averages
from datetime import datetime


def format_date(year, month):
    date = datetime(year, month, 1)
    return datetime.strftime(date, '%m/%d/%Y %I:%M:%S %p')


def format_row(row, value, average):
    formatted_date = format_date(row[0], row[1])
    formatted_row = [row[2], formatted_date, row[3], value, average]
    return formatted_row


def write_rows(ordered_dict, path="output/results.csv"):
    averages = get_monthly_averages(ordered_dict)
    with open(path, 'w') as result_file:
        writer = csv.writer(result_file, delimiter=',')
        for row, average in zip(ordered_dict, reversed(averages)):
            formatted_row = format_row(row, ordered_dict[row], average)
            writer.writerow(formatted_row)


if __name__ == "__main__":
    from src.read_data import read_csv_lines
    read_input = read_csv_lines(path="insight_testsuite/tests/test_1/input/Border_Crossing_Entry_Data.csv")
    write_rows(read_input, path="insight_testsuite/tests/test_2/output/results.csv")

