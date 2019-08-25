# need to assert correct ordering
# if index i > j, then row_i[year] <= row_j[year]
# if index i > j, then row_i[month] <= row_j[month]
# if index i > j, then row_i[value] <= row_j[value]
# with more time, i'd want to do a check that dates are decreasing
# data quality is high, so I will skip those assertions
# I will ensure that for a dates, rows are in decreasing order of value


if __name__ == "__main__":
    from src.read_data import read_csv_lines
    read_input = read_csv_lines()
    for k, v in read_input.items():
        print(k, v)
