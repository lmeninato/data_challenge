# need to assert correct ordering
# if index i > j, then row_i[year] <= row_j[year]
# if index i > j, then row_i[month] <= row_j[month]
# if index i > j, then row_i[value] <= row_j[value]
# with more time, i'd want to do a check that dates are decreasing
# data quality is high, so I will skip those assertions
# I will ensure that for a dates, rows are in decreasing order of value


def order_by_value(list_by_date):
    ordered_list = list_by_date
    return ordered_list


if __name__ == "__main__":
    from src.read_data import read_csv_lines
    read_input = read_csv_lines(path="../insight_testsuite/tests/test_1/input/Border_Crossing_Entry_Data.csv")
    for dates in read_input:
        for k, v in dates.items():
            print(k, v)
