# Python 2.7.5
import os
import urllib2
import base64
import json

# JQL cannot handle non-unicode characters.
# The following 3 lines standardise it (not needed in python3)
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def jql_builder(text, projects=None, upto_date=None):
	return 'text%20~%20\"' + text + '\"' 

def url_builder(host, query):
 	search_call = '/rest/api/2/search?jql='

 	if host.endswith('/'):
 		return host[:-1] + search_call + query
 	return host + search_call + query

# This function cannot handle authentication over a proxy server.
# url is your jira server url/IP
def api_request(username, password, url):
    # basic authentication handler
	try:
	    request = urllib2.Request(url)
	    print request
	except NameError as e:
	    print 'Invalid JQL query.'
	    exit()

	# auth handler
	b64auth = base64.standard_b64encode("%s:%s" % (username, password))
	request.add_header("Authorization", "Basic %s" % b64auth)

	try:
		result = urllib2.urlopen(request)
	except urllib2.HTTPError as e:
		print 'Bad request: please review the credentials supplied.'
		exit()
	
	return json.loads(result.read())
