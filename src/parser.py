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
        if item.isnumeric():
            raise TypeError('Item {} is not a string, it is {}'.format(item, type(item)))
        return item
    else:
        raise TypeError('Item {} is not a string, it is {}'.format(item, type(item)))


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
        return parsed_item
    except (ValueError, TypeError, AttributeError) as e:
        # log error
        print(e)
        print('Failed to parse field at row {}'.format(row_num))
        return -1


def parse_date(date):
    return datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')
