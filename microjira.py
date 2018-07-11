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

# Jira REST API returns A LOT of irrelevant fields.
# Many of them will contain no information whatsoever.
# This is a concise list of the most important fields - 
# it is less than the python jira library can handle
# but for most tasks it is more than enough
def jira_parser(result):
    issue_list = []
    
    if result['total'] > 0:
        print result['total']
        for i in result['issues']:
            issue = {}
            issue['issue_id'] = str(i['key'])
            print issue['issue_id']

            # issue summary // kinda like a name
            issue['summary'] = str(i['fields']['summary'])

            # date created
            issue['created'] = str(i['fields']['created'])[:10] + ' ' + str(i['fields']['created'])[11:19]

            # date updated
            issue['updated'] = str(i['fields']['updated'])[:10] + ' ' + str(i['fields']['updated'])[11:19]

            # priority
            issue['priority'] = str(i['fields']['priority']['name'])

            # resolution if exists
            if i['fields']['resolution']:
                issue['resolution'] = str(i['fields']['resolution']['name'] + ' ' + str(i['fields']['resolution']['description']))

            # environment (can be instance/server) where it happened if available
            if 'environment' in i['fields'] and i['fields']['environment']:
                issue['environment'] = str(i['fields']['environment'])

            # component if such exists
            if 'components' in i['fields']:
                output = []
                # ofile.write('Component: %s\n' % (i['fields']['components'][0]['name']))
                for name in i['fields']['components']:
                    output.append(str(name['name']))
                issue['components'] = ','.join(output)

            # affected versions
            if 'versions' in i['fields']:
                output = []
                # ofile.write('Component: %s\n' % (i['fields']['components'][0]['name']))
                for name in i['fields']['versions']:
                    output.append(str(name['name']))
                issue['versions_affected'] = ' ,'.join(output)

            # fix versions
            if 'fixVersions' in i['fields']:
                output = []
                # ofile.write('Component: %s\n' % (i['fields']['components'][0]['name']))
                for name in i['fields']['fixVersions']:
                    output.append(str(name['name']))
                issue['fix_versions'] = ' ,'.join(output)

            # Full description of the issue
            # Exercise caution: can contain anything that may require
            # further handling and parsing (eg. a Java stack or embedded html) 
            issue['description'] = str(i['fields']['description'])

            issue_list.append(issue)
    else:
        print 'No similar results found in JIRA.'

    return issue_list
