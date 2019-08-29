import csv
from datetime import datetime


def format_date(year, month):
    date = datetime(year, month, 1)
    return datetime.strftime(date, '%m/%d/%Y %I:%M:%S %p')


def format_row(row):
    """
    Formats the tuple, value, and average into the desired row format.
    :param row: [Year, Month, Border, Measure, Value, Average] array
    :return: Formatted row
    """
    formatted_date = format_date(row[0], row[1])
    formatted_row = [row[2], formatted_date, row[3], row[4], row[5]]
    return formatted_row


def get_month_difference(x, y):
    """
    Return number of months between year-month combinations.
    :param x: tuple (year, month)
    :param y: tuple (year, month)
    :return: integer
    """
    return abs((x[0]-y[0])*12 + x[1] - y[1])


def get_monthly_averages(ordered_dict):
    """
    Takes advantage of the hashing the (year, month, border, measure) -> key-value pairs.
    We also have to keep track of the previous total for a given key, and the first occurrence of a key.
    Then the formula: average = (previous total)/(month distance) yields
    the rolling average monthly number of crossings.
    :param ordered_dict: (year, month, border, measure) -> value
    key[0] : Year
    key[1] : Month
    key[2] : Border
    key[3] : Measure
    :return: list of averages
    """
    border_measures = {}
    averages = []
    for key in reversed(ordered_dict):
        temp_key = (key[2], key[3])  # (Border, Measure) tuple
        current_value = ordered_dict[key]
        if temp_key not in border_measures:
            border_measures[temp_key] = {"year-month": (key[0], key[1]), "prev_total": current_value}
            averages.append(0)
        else:
            current_month = (key[0], key[1])
            first_month = border_measures[temp_key]["year-month"]
            prev_total = border_measures[temp_key]["prev_total"]
            month_diff = get_month_difference(first_month, current_month)
            averages.append(-(-prev_total//month_diff))  # round up
            border_measures[temp_key]["prev_total"] += current_value
    return averages


def sort_results(unsorted_dict):
    """
    Sorts by year, month, value, measure, border in descending order.
    Works well on nearly sorted data (O(n) best case).

    key[0] : Year
    key[1] : Month
    key[2] : Border
    key[3] : Measure
    key[4] : Value
    key[6] : Average

    :param unsorted_dict: (year, month, border, measure) -> value
    :return: list of sorted results
    """
    averages = get_monthly_averages(unsorted_dict)
    row_list = []
    for row, average in zip(unsorted_dict, reversed(averages)):
        tuple_as_list = list(row)
        tuple_as_list.extend([unsorted_dict[row], average])
        row_list.append(tuple_as_list)

    return sorted(row_list, key=lambda x: (x[0], x[1], x[4], x[3], x[2]), reverse=True)


def write_rows(ordered_dict, path="output/report.csv"):
    """
    Assuming OrderedDict is mostly sorted for performance.

    Calculates averages from the ordered dict, formats the corresponding (Year, Month, Border, Measure)->Value
    and Average results into the desired row format. Then each row is written to the csv at the inputted path.
    :param ordered_dict: ordered dict of rows grouped by value for (Year, Month, Border, Measure)->Value combinations
    :param path: location of output csv
    :return: None
    """
    with open(path, 'w', newline='') as result_file:
        writer = csv.writer(result_file, delimiter=',')
        writer.writerow(['Border', 'Date', 'Measure', 'Value', 'Average'])
        for row in sort_results(ordered_dict):
            formatted_row = format_row(row)
            writer.writerow(formatted_row)


if __name__ == "__main__":
    from read_data import read_csv_lines
    import sys

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    read_input = read_csv_lines(path=input_path)
    write_rows(read_input, path=output_path)
