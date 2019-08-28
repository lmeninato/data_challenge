import csv
from collections import OrderedDict
from parser import process_row, parse_field, parse_date


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
    [row_num, date.year, date.month, border, measure, value]
    :return: results merged with the new hashed row
    """
    processed_row = process_row(count, row)
    year, month = processed_row[1], processed_row[2]
    border = processed_row[3]
    measure = processed_row[4]
    value = processed_row[5]

    hashed_row = OrderedDict([((year, month, border, measure), value)])

    if processed_row is None:
        # need to log skipped row
        return results
    if not results:
        return hashed_row
    if (year, month, border, measure) in results:
        results[(year, month, border, measure)] += value
    else:
        results[(year, month, border, measure)] = value
    return results


def order_by_value(temp_dict):
    """
    Need the dict key-value pairs to be in the correct order (descending by value).
    :param temp_dict: OrderedDict of measures with the same date
    :return: OrderedDict in correct order
    """
    return OrderedDict(sorted(temp_dict.items(), key=lambda x: x[1], reverse=True))


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


def read_csv_lines(path="../input/Border_Crossing_Entry_Data.csv"):
    """
    Reads in lines and merges into results object. The merge_row function
    defines the logic for aggregating by year, month, border, measure combinations.
    :param path: path of input csv file
    :return: OrderedDict of results
    """
    results = OrderedDict()
    with open(path, 'r') as f:
        data = csv.DictReader(f)
        current_date = (None, None)
        temp_results = OrderedDict()
        for count, row in enumerate(data):
            date = parse_field(parse_date, count, row, 'Date')
            if date == -1:
                continue
            if not all(current_date):
                current_date = (date.year, date.month)
            if current_date == (date.year, date.month):
                temp_results = merge_row(temp_results, count, row)
            else:
                # new date
                temp_results = order_by_value(temp_results)
                results.update(temp_results)
                temp_results = OrderedDict()
                current_date = (date.year, date.month)
                temp_results = merge_row(temp_results, count, row)
        if temp_results != OrderedDict():
            temp_results = order_by_value(temp_results)
            results.update(temp_results)
    return results
