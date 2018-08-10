import requests, json, secrets

def login():
	# import secrets
	baseURL = secrets.baseURL
	user = secrets.user
	password = secrets.password

	# attempt to authenticate
	response = requests.post(baseURL+'/users/'+user+'/login?password='+password+'&expiring=false')

	if response.status_code != 200:
		print('Login failed! Check credentials and try again')
		exit()
	else:
		session = json.loads(response.text)['session']
		headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}
		print('Login successful!')
		return baseURL, headers
