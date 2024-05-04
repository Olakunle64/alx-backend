import csv

with open("Popular_Baby_Names.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)