import json
from guardiankey import checkaccess


## This code snippet must be placed on the page that processes the authentication post 

username = "User"

# function that valide username/password
def authenticate_user():
	return True

# function that make logoff the user
def logoff_user():
	return True

# if valid username/pass, check GuardianKey	
if authenticate_user:
	try:
		result = checkaccess(username)
		if not 'BLOCK' in result['response']:
			print("User authenticated, risk {}".format(result['risk']))
		else:
			print("User logoff, risk: {}".format(result['risk']))
			logoff_user()
	except ValueError as e:
		print("User authenticated, without GuardianKey response")
		
# if not valid user/pass, inform GuardianKey		
else:
	sendevent(username,'',1)
