import json
import base64
import time
import socket
import requests
from Crypto.Cipher import AES
from _socket import timeout

# Please run register.py for generate your configuration,
#  or take this info at panel.guardiankey.io
GKconfig = {}
GKconfig['agentid'] = ''
GKconfig['key']     = ''
GKconfig['iv']      = ''
GKconfig['service'] = 'MySystem'
GKconfig['orgid']   = ''
GKconfig['authgroupid'] = ''
GKconfig['reverse'] = True

# You need define how the your system get client informations (IP, User-agent):
def getClientIP():
    #...
    ip = "1.1.1.1" # SET-ME
    return ip

def getUserAgent():
    #...
    UA="Set-me"
    return UA

def create_message(username,userEmail="",loginfailed=0,eventType='Authentication'):
    global GKconfig
    keyb64      = GKconfig['key']
    ivb64       = GKconfig['iv']
    agentid     = GKconfig['agentid']
    orgid       = GKconfig['orgid']
    authgroupid = GKconfig['authgroupid']
    reverse     = GKconfig['reverse']
    timestamp   = int(time.time())
    
    if agentid is not None:
        key = base64.b64decode(keyb64)
        iv  = base64.b64decode(ivb64)
        clientIP = getClientIP()
        UA = getUserAgent()
        sjson = {}
        sjson['generatedTime'] = timestamp
        sjson['agentId'] = agentid
        sjson['organizationId'] = orgid
        sjson['authGroupId'] = authgroupid
        sjson['service'] = GKconfig['service']
        sjson['clientIP'] = clientIP
        try:
            sjson['clientReverse'] = socket.gethostbyaddr(clientIP)[0] if reverse else ""
        except:
            sjson['clientReverse'] = ""
        sjson['userName'] = username
        sjson['authMethod'] = ''
        sjson['loginFailed'] = str(loginfailed)
        sjson['userAgent'] = UA
        sjson['psychometricTyped'] = ''
        sjson['psychometricImage'] = ''
        sjson['event_type'] = eventType
        sjson['userEmail'] = userEmail
        message = json.dumps(sjson)
        obj = AES.new(key,AES.MODE_CFB, iv, segment_size=8)
        cryptmessage = base64.b64encode(obj.encrypt(message)).decode('ascii')
        return cryptmessage
        
def sendeventUDP(username,userEmail="",loginfailed=0,eventType='Authentication'):
    global GKconfig
    message = create_message(username,userEmail,loginfailed,eventType)
    payload = GKconfig['authgroupid']+"|"+message
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(payload, ('collector.guardiankey.net', 8888))

def sendevent(username,userEmail="",loginfailed=0,eventType='Authentication'):
    global GKconfig
    message = create_message(username,userEmail,loginfailed,eventType)
    tmpdata = {}
    tmpdata['id'] = GKconfig['authgroupid']
    tmpdata['message'] = message
    data = json.dumps(tmpdata)
    url = 'https://api.guardiankey.io/sendevent'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        requests.post(url, data=data, headers=headers, timeout=4)
        return ""
    except:
        return ""

def checkaccess(username,userEmail="",loginfailed=0,eventType='Authentication'):
    global GKconfig
    message = create_message(username,userEmail,loginfailed,eventType)
    tmpdata = {}
    tmpdata['id'] = GKconfig['authgroupid']
    tmpdata['message'] = message
    data = json.dumps(tmpdata)
    url = 'https://api.guardiankey.io/checkaccess'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        query = requests.post(url, data=data, headers=headers, timeout=4)
        gkreturn = json.loads(query.text)
        return gkreturn
    except:
        return {"response":"ERROR"}


