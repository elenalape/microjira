import os
import urllib2
import base64
import json

def jira_authenticator(username, password, server):
    
    # basic authentication handler
    b64auth = base64.standard_b64encode("%s:%s" % (username, password))
    request.add_header("Authorization", "Basic %s" % b64auth)

    try:
        result = urllib2.urlopen(server)
    except urllib2.HTTPError as e:
        print 'Jira authentication failed. Please review the credentials supplied.'
        exit()

    return True
