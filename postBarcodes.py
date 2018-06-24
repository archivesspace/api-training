import json, requests, csv, authenticate, runtime
# since we're going to re-use the baseURL and headers variables, we'll import them here
from authenticate import baseURL, headers

# print instructions
print ('This script replaces existing fauxcodes with real barcodes (linked in a separate csv file) in ArchivesSpace.')
input('Press Enter to connect to ArchivesSpace and post those barcodes...')

# This is where we connect to ArchivesSpace.  See authenticate.py
authenticate.test_connection()

# open csv and generate dict
reader = csv.DictReader(open('barcodes.csv'))

# GET each top_container listed in top_containers and add to records
print ('The following barcodes have been updated in ArchivesSpace:')
for row in reader:
	uri = row['uri']
	output = requests.get(baseURL + uri, headers=headers).json()
	output['barcode'] = row['real']
	post = requests.post(baseURL + uri, headers=headers, data=json.dumps(output)).json()
	print (post)
