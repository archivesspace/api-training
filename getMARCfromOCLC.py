import pathlib, requests, supersecrets, runtime

print("Demo: you can use this simple script to download MARC records from OCLC. However, you will need an API key to authenticate. Once you have one, you can update the 'wskey' variable.")

# See: https://platform.worldcat.org/api-explorer/apis/wcapi

oclcURL = 'http://www.worldcat.org/webservices/catalog/content/'

wskey = supersecrets.wskey

oclc_numbers = []
oclc_numbers.extend(('647845821', '648010759', '51024910', '647834263', '647909502', '647824468', '647844488', '34336539'))

pathlib.Path('marc-files').mkdir(exist_ok=True)

for num in oclc_numbers:
    response = requests.get(oclcURL + num + '?wskey=' + wskey)
    with open('marc-files/'+num+'.xml', 'wb') as file:
        file.write(response.content)
        file.close()
