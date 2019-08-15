import csv


# implement this
def analyze_function():
    return None


if __name__ == '__main__':
    with open("random.csv") as f:
        data = csv.DictReader(f)
        for row in data:
            print(row['A'])
