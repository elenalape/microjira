# Python 2.7.5
import os
import urllib2
import base64
import json

# JQL cannot handle non-unicode characters.
# The following 3 lines standardise it.
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# This function cannot handle authentication over a proxy server.
# server is your jira server url/IP
def jira_authenticator(username, password, server):
    
    # Basic authentication handler
    b64auth = base64.standard_b64encode("%s:%s" % (username, password))
    request.add_header("Authorization", "Basic %s" % b64auth)

    try:
        request = urllib2.Request(server)
    except urllib2.HTTPError as e:
        print 'Jira authentication failed. Please review the credentials supplied.'
        exit()

    return True
