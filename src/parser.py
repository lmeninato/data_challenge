from datetime import datetime


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
    border = parse_field(parse_str_field, row_num, data_row, 'Border')
    measure = parse_field(parse_str_field, row_num, data_row, 'Measure')
    value = parse_field(parse_int_field, row_num, data_row, 'Value')

    res = [row_num, date.year, date.month, border, measure, value]
    if None in res:
        return None
    return res


def parse_int_field(item):
    item = int(item)
    if item < 0:
        raise ValueError('Item {} is negative'.format(item))
    return item


def parse_str_field(item):
    if isinstance(item, str):
        return item
    else:
        raise TypeError('Item {} is not string, it is {}'.format(item, type(item)))


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
        # log error
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        return None
    except ValueError:
        # log error
        print('Failed to parse field {0} with value {1} at row {2}'.format(field, item, row_num))
        return None
    except TypeError:
        # log error
        print('Failed to parse field {0} with value {1} at row {2}'.format(field, item, row_num))
        return None
    return parsed_item


def parse_date(date):
    return datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')