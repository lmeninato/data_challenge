import csv
from read_data import get_monthly_averages
from datetime import datetime


def format_date(year, month):
    date = datetime(year, month, 1)
    return datetime.strftime(date, '%m/%d/%Y %I:%M:%S %p')


def format_row(row, value, average):
    """
    Formats the tuple, value, and average into the desired row format.
    :param row: (Year, Month, Border, Measure)  tuple
    :param value: hashed value corresponding to row tuple
    :param average: average corresponding to row tuple
    :return: Formatted row
    """
    formatted_date = format_date(row[0], row[1])
    formatted_row = [row[2], formatted_date, row[3], value, average]
    return formatted_row


def write_rows(ordered_dict, path="output/report.csv"):
    """
    Calculates averages from the ordered dict, formats the corresponding (Year, Month, Border, Measure)->Value
    and Average results into the desired row format. Then each row is written to the csv at the inputted path.
    :param ordered_dict: ordered dict of rows grouped by value for (Year, Month, Border, Measure)->Value combinations
    :param path: location of output csv
    :return: None
    """
    averages = get_monthly_averages(ordered_dict)
    with open(path, 'w', newline='') as result_file:
        writer = csv.writer(result_file, delimiter=',')
        writer.writerow(['Border', 'Date', 'Measure', 'Value', 'Average'])
        for row, average in zip(ordered_dict, reversed(averages)):
            formatted_row = format_row(row, ordered_dict[row], average)
            writer.writerow(formatted_row)


if __name__ == "__main__":
    from read_data import read_csv_lines
    import sys

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    read_input = read_csv_lines(path=input_path)
    write_rows(read_input, path=output_path)

