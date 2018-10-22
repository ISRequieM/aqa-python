from jira.jira import *
import allure

username = JiraParameters.user
user_password = JiraParameters.password
project_key = JiraParameters.project_key


@allure.epic('Jira REST API')
@allure.title('Login using wrong password')
def test_wrong_password():
    jira_wrong_password = JiraRestActions(username, user_password+"01", project_key)
    assert jira_wrong_password.authenticate().get("success") == False


@allure.epic('Jira REST API')
@allure.title('Login using wrong username')
def test_wrong_username():
    jira_wrong_user = JiraRestActions(username+"01", user_password, project_key)
    assert jira_wrong_user.authenticate().get("success") == False


@allure.epic('Jira REST API')
@allure.title('Login')
def test_correct_credentials():
    jira_actions = JiraRestActions(username, user_password, project_key)
    assert jira_actions.authenticate().get("success") == True

