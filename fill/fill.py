import time
import csv
import re
import requests
import os

url_pipeline = 'http://0.0.0.0:9200/_ingest/pipeline/projet_3_pipeline'
url_index = 'http://0.0.0.0:9200/projet_3'
headers = {'Content-Type': 'application/json'}

header_name = []

def transform():
	global header_name
	input_file = open('top250-00-19.csv', 'r')
	output_file = open('top250-00-19_modified.csv', 'w')
	data = csv.reader(input_file)
	writer = csv.writer(output_file)

	header_name = next(data, None)
	for line in data:
		line = [value.replace('"', '') for value in line]
		line = [value.replace(',', '') for value in line]
		line = [value.replace('-', '') for value in line]
		line = [value.replace(';', '') for value in line]
		line = [re.sub(r"^\d\.\s?", '', value) for value in line]
		line = [value.replace('\n', '').strip() for value in line]
		line = [value.replace('\'', '') for value in line]
		line = [value.replace('NA', '') for value in line]
		writer.writerow(line)

	input_file.close()
	output_file.close()

def create_pipeline():
	data = {"processors":[{"csv":{'field':"csv_line","target_fields":header_name}}]}
	r = requests.put(url_pipeline, headers=headers, json=data)

def create_index():
	data = open('projet_3_analyzer.json', 'rb')
	r = requests.put(url_index, headers=headers, data=data)

def exe_script():
	os.system('./insert.sh')

transform()
time.sleep(5)
create_pipeline()
time.sleep(5)
create_index()
time.sleep(10)
exe_script()
