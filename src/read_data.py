import csv
from datetime import datetime
from collections import OrderedDict


def merge_row(results, count, row):
    """
    I hash the tuple by which we aggregate the number of crossings.
    This allows for searching for the (date, border, measure)
    combination upon which to aggregate in O(1) time.

    Similarly, looking for the previous month's value to calculate
    the running average can be done in O(1) time, since we just have
    to check for the same key but with month = month - 1.
    :param results: Contains aggregated hashed rows
    :param count: line number in csv file
    :param row: row of csv files corresponding to the count param
    :return: results merged with the new hashed row
    """
    # could return an OrderedDict to clean this up
    processed_row = process_row(count, row)
    year, month = processed_row[1], processed_row[2]
    border = processed_row[3]
    measure = processed_row[5]
    value = processed_row[6]

    hashed_row = OrderedDict([((year, month, border, measure), value)])

    if processed_row is None:
        return results
    if not results:
        return hashed_row
    if (year, month, border, measure) in results:
        results[(year, month, border, measure)] += value
    else:
        results[(year, month, border, measure)] = value
    return results


def process_row(row_num, data_row):
    """
    Parses each field in row and returns appends to results.
    :param row_num: row number
    :param data_row: row of data to be processed
    :return: Returns all the fields desired in the results dict
    """
    date = parse_field(parse_date, row_num, data_row, 'Date')
    if date is None:
        return None
    formatted_date, year, month = format_date(date), date.year, date.month
    border = parse_field(parse_str_field, row_num, data_row, 'Border')
    measure = parse_field(parse_str_field, row_num, data_row, 'Measure')
    value = parse_field(parse_int_field, row_num, data_row, 'Value')

    res = [row_num, date.year, date.month, border, formatted_date, measure, value]
    if None in res:
        return None
    return res


def parse_int_field(item):
    item = int(item)
    return item


def parse_str_field(item):
    if isinstance(item, str):
        return item
    else:
        return None


def parse_field(parser, row_num, data_row, field):
    """
    Checks to make sure the data is parsed correctly.

    :param parser: function to check for type, data validation, etc.
    :param row_num: row number
    :param data_row: row of data
    :param field: desired field to parse
    :return: field value
    """
    item = data_row[field]
    try:
        parsed_item = parser(item)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        return None
    except ValueError:
        print('Failed to parse field {0} with value {1} at row {2}'.format(field, item, row_num))
        return None
    return parsed_item


def parse_date(date):
    return datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')


def format_date(date):
    return datetime.strftime(date, '%m/%d/%Y %I:%M:%S %p')


def binary_search(rows, row):
    val_index = -1
    mid = len(rows) // 2
    if rows[mid][val_index] > row[val_index]:
        return binary_search(rows[mid:], row)
    elif rows[mid][val_index] < row[val_index]:
        return binary_search(rows[:mid], row)
    else:
        return mid


def order_by_value(temp_dict):
    ordered_results = []
    for measures, value in temp_dict.items():
        row = list(measures)
        row.append(value)
        ordered_results.append(row)
    ordered_results.sort(key=lambda x: x[-1], reverse=True)
    return ordered_results


def read_csv_lines(path="../input/Border_Crossing_Entry_Data.csv"):
    """
    Reads in lines and merges into results object. The merge_row function
    defines the logic for aggregating by year, month, border, measure combinations.
    :param path: path of input csv file
    :return: OrderedDict of results
    """

    # header = [['Index', 'Year', 'Month', 'Border', 'Date', 'Measure', 'Value', 'Average']]
    results = []
    with open(path, 'r') as f:
        data = csv.DictReader(f)
        current_date = (None, None)
        temp_results = OrderedDict()
        for count, row in enumerate(data):
            try:
                date = parse_field(parse_date, count, row, 'Date')
                if not all(current_date):
                    current_date = (date.year, date.month)
                if current_date == (date.year, date.month):
                    temp_results = merge_row(temp_results, count, row)
                else:
                    # current_date != date
                    temp_results = order_by_value(temp_results)
                    results.extend(temp_results)
                    temp_results = OrderedDict()
                    current_date = (date.year, date.month)
                    temp_results = merge_row(temp_results, count, row)
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
                print("Saving results, error occurred at row number: {}".format(count))
        if temp_results != OrderedDict():
            temp_results = order_by_value(temp_results)
            results.extend(temp_results)
    # iterate through results writing to results.csv
    return results


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(read_csv_lines(path=sys.argv[1]))
    else:
        print(read_csv_lines(path="insight_testsuite/tests/test_1/input/Border_Crossing_Entry_Data.csv"))
