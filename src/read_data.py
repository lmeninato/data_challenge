import csv
from datetime import datetime
from collections import OrderedDict


def merge_row(results, count, row):
    """
    I hash the tuple by which we aggregate the number of crossings.
    This allows for searching for the (date, border, measure)
    combination upon which to aggregate in O(1) time.

    :param results: Contains aggregated hashed rows
    :param count: line number in csv file
    :param row: row of csv files corresponding to the count param
    :return: results merged with the new hashed row
    """
    processed_row = process_row(count, row)
    year, month = processed_row[1], processed_row[2]
    border = processed_row[3]
    measure = processed_row[5]
    value = processed_row[6]

    # user OrderedDict?
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


def group_by_month(processed_row):
    """
    :param processed_row result from process_row()
    :return:
    """
    return None


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
    try:
        item = int(item)
        return item
    except ValueError:
        raise ValueError


def parse_str_field(item):
    if isinstance(item, str):
        return item
    else:
        return None


def parse_field(parser, row_num, data_row, field):
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


def read_csv_lines(path="../input/Border_Crossing_Entry_Data.csv"):
    # header = [['Index', 'Year', 'Month', 'Border', 'Date', 'Measure', 'Value', 'Average']]
    results = OrderedDict()
    with open(path, 'r') as f:
        data = csv.DictReader(f)
        for count, row in enumerate(data):
            try:
                results = merge_row(results, count, row)
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
                print("Saving results, error occurred at row number: {}".format(count))
    # iterate through results writing to results.csv
    return results


if __name__ == '__main__':
    read_csv_lines(path="../insight_testsuite/tests/test_1/input/Border_Crossing_Entry_Data.csv")
