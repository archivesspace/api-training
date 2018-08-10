import requests, authenticate, json, glob, runtime, sys
from pathlib import Path

baseURL, headers = authenticate.login()

directory = "uva-marc-files"
repository = "2"
max_files = 10
import_type = "marcxml"
file_list = []
filenames = []
for f in glob.iglob(directory + '/*.xml'):
    filename = Path(f).stem
    file_list.append(("files[]", open(f, "rb")))
    filenames.append(filename)
if len(filenames) > max_files:
    print("Woah. Let's not get too crazy.  Try again with less files, or update this script so that it will split up the jobs so that each post has no more than {0} files each.".format(max_files))
    sys.exit(1)

print("Okay. We're going to upload the following filenames: {0}".format(filenames))

job = json.dumps(
        {
            "job_type": "import_job",
            "job": {
                "import_type": import_type,
                "jsonmodel_type": "import_job",
                "filenames": filenames
            }
        }
    )

upload = requests.post(baseURL + "/repositories/" + repository + "/jobs_with_files"
, files=file_list
, params={"job": job}
, headers=headers).json()

print("Import job started...")
print("\nCheck out " + baseURL + upload['uri'] + " in ArchivesSpace.\n")
