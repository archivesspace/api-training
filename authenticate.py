import requests, json, secrets
from requests.compat import urljoin, quote

def login():
	# import secrets
	baseURL = secrets.baseURL
	user = secrets.user
	password = secrets.password

	# attempt to authenticate
	# following the approach used in ArchivesSnake
	response = requests.post(urljoin(baseURL, '/users/{user}/login'.format(user=quote(user))),
		params={"password": password, "expiring": False})

	if response.status_code != 200:
		print('Login failed! Check credentials and try again')
		exit()
	else:
		session = json.loads(response.text)['session']
		headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}
		print('Login successful!')
		return baseURL, headers
