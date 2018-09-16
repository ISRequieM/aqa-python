from phase02.json_fixtures import *
from phase02.jira import *
import requests
username = JiraParameters.user
user_password = JiraParameters.password
project_key = JiraParameters.project_key

def test_wrong_password():
    jira_wrong_password = JiraRestActions(username, user_password+"01", project_key)
    assert jira_wrong_password.authenticate() == "Failed"

def test_wrong_username():
    jira_wrong_user = JiraRestActions(username+"01", user_password, project_key)
    assert jira_wrong_user.authenticate() == "Failed"

def test_correct_credentials():
    jira_actions = JiraRestActions(username, user_password, project_key)
    assert jira_actions.authenticate() != "Failed"

