if __name__ == "__main__":

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    username, password = '', ''
    
    text = raw_input('Enter your JQL query:')
    
    query = jql_builder(projects, date, text)

    url = url_builder('https://jira.example.com/', query)
    
    result = api_request(username, password, url)

    jira_issues = jira_parser(result)

    with open('data.txt', 'w') as file:
        for i in jira_issues:
            file.write('ID: ' + str(i['issue_id']) + '\n')
            file.write('Summary: ' + str(i['summary']) + '\n')
            file.write('Created: ' + str(i['created']) + '\n')
            file.write('Updated: ' + str(i['updated']) + '\n')
            file.write('Description: ' + str(i['description']) + '\n')
            file.write('--------------------------------\n')

