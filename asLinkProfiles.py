import json, requests, authenticate, runtime
# since we're going to re-use the baseURL and headers variables, we'll import them here
from authenticate import baseURL, headers

# function to find key in nested dictionaries: see http://stackoverflow.com/questions/9807634/find-all-occurences-of-a-key-in-nested-python-dictionaries-and-lists
# and now we're getting fancy!
def gen_dict_extract(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

# This is where we connect to ArchivesSpace.  See authenticate.py
authenticate.test_connection()

# provide instructions
print ('This script is used to link all top_containers in a single collection (identified by the ArchivesSpace resource ID number) to a single container_profile (identified by the ArchivesSpace container_profile ID number).')
input('Press Enter to continue...')

# have user enter resource id
resource_id = input('Enter resource ID (in this case, you should enter 1): ')

# search for top_containers linked to entered resource id
endpoint = '/repositories/2/top_containers/search?page=1&aq={"filter_term":{"field":"collection_uri_u_sstr", "value":"/repositories/2/resources/ + resource_id", "jsonmodel_type":"field_query"}}'
output = requests.get(baseURL + endpoint, headers=headers).json()

# populate top_containers with the ids of each top_container in search results
top_containers = []
for value in gen_dict_extract('id', output):
    top_containers.append(value)

# GET each top_container listed in top_containers and add to records
records = []
for top_container in top_containers:
    output = requests.get(baseURL + top_container, headers=headers).json()
    records.append(output)

# have user enter container profile id
profile_id = input('Enter container profile ID (I am going to enter 9. You can select another value, as long that ID is in your instance of ArchivesSpace.): ')

# Add container profile to records and post
print ('The following records have been updated in ArchivesSpace:')
for record in records:
    record['container_profile'] = {'ref': '/container_profiles/' + profile_id}
    jsonLine = json.dumps(record)
    uri = record['uri']
    post = requests.post(baseURL + uri, headers=headers, data=jsonLine).json()
    print(post)
