import csv

prt = print
ask = input

with open("data.csv", "r") as file:
    reader = csv.reader(file)
    #prt(list(reader))
    for row in reader:
        prt(row)