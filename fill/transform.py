import csv
import re

input_file = open('top250-00-19.csv', 'r')
output_file = open('top250-00-19_modified.csv', 'w')
data = csv.reader(input_file)
writer = csv.writer(output_file)

next(data,None)
for line in data:
    line = [value.replace('"', '') for value in line]
    line = [value.replace(',', '') for value in line]
    line = [value.replace(';', '') for value in line]
    line = [value.replace('-', ' ') for value in line]
    line = [re.sub(r"^\d\.\s?", '', value) for value in line]
    line = [value.replace('\n', '').strip() for value in line]
    line = [value.replace('\'', '') for value in line]
    line = [value.replace('NA', '') for value in line]
    writer.writerow(line)

input_file.close()
output_file.close()
