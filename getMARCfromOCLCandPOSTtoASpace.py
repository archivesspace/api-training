import pathlib, authenticate, requests, json, glob, supersecrets, runtime, sys

print("Demo: you can use this simple script to download MARC records from OCLC. However, you will need an API key to authenticate. Once you have one, you can update the 'wskey' variable.")

# See: https://platform.worldcat.org/api-explorer/apis/wcapi

oclcURL = 'http://www.worldcat.org/webservices/catalog/content/'
directory = "marc-files"
wskey = supersecrets.wskey

oclc_numbers = []
oclc_numbers.extend(('647845821', '648010759', '51024910', '647834263', '647909502', '647824468', '647844488', '34336539'))

pathlib.Path(directory).mkdir(exist_ok=True)

for num in oclc_numbers:
    response = requests.get(oclcURL + num + '?wskey=' + wskey)
    with open(directory+'/'+num+'.xml', 'wb') as file:
        file.write(response.content)
        file.close()

print("\nNow that we've downloaded the MARC files. Let's post them to ArchivesSpace.\n")

repository = "2"
max_files = 10
import_type = "marcxml"
file_list = []
for f in glob.iglob(directory + '/*.xml'):
    file_list.append(("files[]", open(f, "rb")))
if len(oclc_numbers ) > max_files:
    print("Woah. Let's not get too crazy.  Try again with less files, or update this script so that it will split up the jobs so that each post has no more than {0} files each.".format(max_files))
    sys.exit(1)

print("Okay. We're going to upload the following filenames: {0}".format(oclc_numbers))

if not input("Are you sure? (y/n): ").lower().strip()[:1] == "y":
    print("You'd be wise to check out the MARC files first, anyway!")
    sys.exit(1)

baseURL, headers = authenticate.login()

job = json.dumps(
        {
            "job_type": "import_job",
            "job": {
                "import_type": import_type,
                "jsonmodel_type": "import_job",
                "filenames": oclc_numbers
            }
        }
    )

upload = requests.post(baseURL + "/repositories/" + repository + "/jobs_with_files"
, files=file_list
, params={"job": job}
, headers=headers).json()

print("Import job started...")
print("\nCheck out " + baseURL + upload['uri'] + " in ArchivesSpace.\n")
