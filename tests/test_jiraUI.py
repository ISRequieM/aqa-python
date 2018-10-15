import pytest
from webdriver_manager.chrome import ChromeDriverManager

from jira.jira import JiraParameters
from pages.CreateIssuePage import CreateIssuePage
from pages.LoginPage import LoginPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jira.jira import JiraRestActions


chrome_options = Options()
chrome_options.add_argument("--headless")
#driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.set_page_load_timeout(10)
driver.set_script_timeout(10)
login_page = LoginPage(driver)
create_page = CreateIssuePage(driver)
issue_keys = {}
user = JiraParameters.user
password = JiraParameters.password
project_key = JiraParameters.project_key
rest_actions = JiraRestActions(user, password, project_key)


def test_jira_login_wrong_password():
    assert login_page.login_to_jira_creds_privided(JiraParameters.user, "admin") == False


def test_jira_login_wrong_username():
    assert login_page.login_to_jira_creds_privided("admin", JiraParameters.password) == False


def test_jira_login():
    assert login_page.login_to_jira() == True


def test_create_issue():
    issue_keys["0"] = create_page.create_issue(project="AQAPYTHON", issue_type="Bug", summary="some_summary")
    assert issue_keys.__sizeof__() > 0
    print(issue_keys.get("0"))


def test_cleanup():
    driver.quit()
    assert rest_actions.authenticate() != "Failed"
    assert rest_actions.delete_issue(issue_keys.get("0")).get("success") == True





