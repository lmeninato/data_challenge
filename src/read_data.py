import csv
from datetime import datetime
from collections import OrderedDict


def append_row(dataframe, processed_row):
    return None


def group_by_month(processed_row):
    """
    :param processed_row result from process_row()
    :return:
    """
    header.append(processed_row)


def process_row(row_num, data_row):
    """
    Parses each field in row and returns appends to results.
    :param row_num: row number
    :param data_row: row of data to be processed
    :return: Returns all the fields desired in the results dict
    """
    date = parse_field(parse_date, row_num, data_row, 'Date')
    formatted_date = None
    if date is not None:
        formatted_date, year, month = format_date(date), date.year, date.month

    border = parse_field(parse_str_field, row_num, data_row, 'Border')
    measure = parse_field(parse_str_field, row_num, data_row, 'Measure')
    value = parse_field(parse_str_field, row_num, data_row, 'Value')

    return OrderedDict([('Year', date.year), ('Month', date.month), ('Border', border), ('Date', formatted_date),
                        ('Measure', measure), ('Value', value), ('Average', 0)])


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


if __name__ == '__main__':
    header = [['Year', 'Month', 'Border', 'Date', 'Measure', 'Value', 'Average']]
    results = {'Year': [], 'Month': [], 'Border': [], 'Date': [], 'Measure': [], 'Value': [], 'Average': []}
    with open("../input/Border_Crossing_Entry_Data.csv") as f:
        data = csv.DictReader(f)
        for count, row in enumerate(data):
            print(process_row(count, row))
