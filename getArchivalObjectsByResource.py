import json, requests, authenticate, runtime

def findKey(d, key):
    if key in d:
        yield d[key]
    for k in d:
        if isinstance(d[k], list) and k == 'children':
            for i in d[k]:
                for j in findKey(i, key):
                    yield j


# This is where we connect to ArchivesSpace.  See authenticate.py
baseURL, headers = authenticate.login()

repoID = input('Enter repository ID:' )
resourceID = input('Enter resource ID: ')

endpoint = '/repositories/'+repoID+'/resources/'+resourceID+'/tree'

try:
    output = requests.get(baseURL + endpoint, headers=headers).json()
except requests.exceptions.RequestException as e:
    print ("Invalid URL. Try running the script again with different repository and/or resource numbers.")
    exit()

archivalObjects = []
for value in findKey(output, 'record_uri'):
    if 'archival_objects' in value:
        archivalObjects.append(value)

records = []
for archivalObject in archivalObjects:
    output = requests.get(baseURL + archivalObject, headers=headers).json()
    records.append(output)

f=open('archivalObjectsFromResource'+resourceID+'.json', 'w')
json.dump(records, f)
f.close()
