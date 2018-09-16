import requests
import json
from phase02.json_fixtures import *
from phase02.jira import *
from phase02.json_fixtures import *

# def test_login_to_jira():
#
#     jiraUrl='http://jira.hillel.it:8080/rest/auth/1/session'
#
#     auth_data = getauthjson("Ilya_Sotnik", "Installed_12345")
#     headers = get_contenttype_header("json")
#     r = requests.post(jiraUrl, json=auth_data, headers=headers)
#     print("STATUS CODE: " + str(r.status_code))
#     #print("Responce is: " + str(r.content))
#     print("Responce is: ")
#     responceJson = json.loads(str(r.text))
#     print(responceJson)
#     print("JSESSIONID = : "+str(responceJson.get("session").get("value")))
#     assert r.status_code == 200


#test_login_to_jira()
#print(JiraRestActions.authenticate(JiraRestActions))

values = {'summary': 'some_summary', 'description': 'some_description'}


jira_action = JiraRestActions(user=JiraParameters.user, password=JiraParameters.password, projectKey=JiraParameters.project_key)
session_id = jira_action.authenticate()
print(session_id)
print(jira_action.createIssue(issueType="Bug", projectKey=JiraParameters.project_key, issue_fields=values))
