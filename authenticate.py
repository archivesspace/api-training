import requests, time, secrets

# import secrets
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

#authenticate
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

# test for successful connection
def test_connection():
	try:
		requests.get(baseURL)
		print ('Connected!')
		return True

	except requests.exceptions.ConnectionError:
		print ('Connection error. Please confirm ArchivesSpace is running.  Trying again in 10 seconds.')

is_connected = test_connection()

while not is_connected:
	time.sleep(10)
	is_connected = test_connection()
