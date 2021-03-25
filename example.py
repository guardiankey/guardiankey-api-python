from guardiankey import checkaccess

'''
   Diagram of the authentication flow with GuardianKey
   ===================================================

          notify user: invalid credentials
    |--<--------------------------<-------------------------<--|
    |                                                          |
    |                                                 NO       |
  User ----> Authenticate ----> <Valid credentials?> ----> Notify GuardianKey
    |                                    | YES
    |                                    |
    |                             Check GuardianKey
    |                                    |           NO
    |                             <Should BLOCK?> --------> Proceed w/ authentication
    |                                    | YES
    --<--------------<----------------<--|
      notify user: invalid credentials

'''

## This code snippet must be placed on the page that processes the authentication post 

# Example user submitted
username = "user@domainxpto.com"
useremail= username

# function that valide username/password
def is_credentials_valid():
    # user exists and password match
    return True

# function that make logout the user
def logout_user():
    # Clean session
    return True

## When user/pass submitted:

if is_credentials_valid():
    try: # YES
        # Check GuardianKey
        result = checkaccess(username,useremail)
        # print(result) # use if you want to see the return
        if result['response'] == 'BLOCK':
            # GuardianKey returned to BLOCK
            logout_user()
            print("User logout. GuardianKey risk: {}".format(result['risk']))
        else:
            # GuardianKey returned not BLOCK (low risk cases)
            print("User authenticated. GuardianKey risk {}".format(result['risk']))
            # Proceed with authentication
    except Exception as e:
        # Something went wrong. Continue in any case!
        print("User authenticated, without GuardianKey response")
        # Proceed with authentication

# if not valid user/pass, inform GuardianKey		
else:
    checkaccess(username,useremail,1)
    # Return to user: invalid credentials....


'''
Attention:
 1) you should implement functions getClientIP() and getUserAgent()
   in guardiankey.py based on your case.
 2) requirements:
     pip install pycrypto
'''
