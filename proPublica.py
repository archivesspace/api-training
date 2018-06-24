import json, requests, runtime

# print instructions
print ('This script creates and saves a separate file called "proPublicaRecord.json" containing the results of a proPublica search for "animal."')
input('Press Enter to continue...')

endpoint = 'http://projects.propublica.org/nonprofits/api/v2/search.json?q=animal'
output = requests.get(endpoint).json()
f=open('proPublicaRecord.json', 'w')
results=(json.dump(output, f))
f.close()
