import time
import allure
import pytest
from allure_commons.types import AttachmentType
from webdriver_manager.chrome import ChromeDriverManager
import inspect

from jira.jira import JiraParameters
from pages.CreateIssuePage import CreateIssuePage
from pages.LoginPage import LoginPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jira.jira import JiraRestActions
from pages.SearchIssuePage import SearchIssuePage
from pages.IssuePage import IssuePage


class Test_JiraUI:
    driver = None
    login_page = None
    create_page = None
    issue_key = None
    issues = {}
    rest_actions = None
    issue_filter_page = None
    issue_page = None

    @pytest.fixture(scope="function")
    def setup(self, request):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options) # doesn't work in circle ci container
        self.driver = webdriver.Chrome(options=chrome_options)
        #self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(20)
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(20)
        self.driver.set_window_size(1440, 900)
        self.login_page = LoginPage(self.driver)
        self.create_page = CreateIssuePage(self.driver)
        self.issue_filter_page = SearchIssuePage(self.driver)
        self.issue_page = IssuePage(self.driver)
        user = JiraParameters.user
        password = JiraParameters.password
        project_key = JiraParameters.project_key
        self.rest_actions = JiraRestActions(user, password, project_key)

        def fin():
            print("\nPerforming tear down")
            self.driver.quit()
            assert self.rest_actions.authenticate().get("success")
            for key in self.issues.values():
                assert self.rest_actions.delete_issue(key).get("success")
            self.issues = {}
        request.addfinalizer(fin)
        print("\nSetup was performed")

    @allure.epic('Jira WebUI')
    @allure.title('Test-UI-Login-Wrong-Password')
    @allure.description('Rest API authorization with wrong password')
    def test_jira_login_wrong_password(self, setup):
        assert self.login_page.login_to_jira_creds_privided(JiraParameters.user, "admin") == False
        allure.attach(name=inspect.stack()[0][3], body=self.driver.get_screenshot_as_png(), attachment_type=AttachmentType.PNG)

    @allure.epic('Jira WebUI')
    @allure.title('Test-UI-Login-Wrong-Username')
    @allure.description('Rest API authorization using wrong username')
    def test_jira_login_wrong_username(self, setup):
        assert self.login_page.login_to_jira_creds_privided("admin", JiraParameters.password) == False
        allure.attach(name="Error when login with wrong user name", body=self.driver.get_screenshot_as_png(),
                      attachment_type=AttachmentType.PNG)

    @allure.epic('Jira WebUI')
    @allure.title('Test-UI-Create-Missing-Required-Field')
    @allure.description('Jira UI create issue with missing summary')
    def test_create_issue_missing_summary(self, setup):
        assert self.login_page.login_to_jira() == True
        result = self.create_page.create_issue(project="AQAPYTHON", issue_type="Bug", summary="")
        allure.attach(name="Creating issue with missing summary", body=self.driver.get_screenshot_as_png(),
                      attachment_type=AttachmentType.PNG)
        assert result.get("success") == False
        assert result.get("issue_key") is None
        assert result.get("error_in_field") == "summary"
        assert result.get("error_message") == "You must specify a summary of the issue."

    @allure.epic('Jira WebUI')
    @allure.title('Test-UI-Create-Too-Long-Field')
    @allure.description('Jira UI create issue with too long summary')
    def test_create_issue_too_long_summary(self, setup):
        assert self.login_page.login_to_jira() == True
        summary = 'some_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarys' + \
                  'ome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysom' + \
                  'e_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_s' + \
                  'ummarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summa' + \
                  'rysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome' + \
                  '_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summary' + \
                  'some_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summary'
        result = self.create_page.create_issue(project="AQAPYTHON", issue_type="Bug", summary=summary)
        allure.attach(name="Creating issue with too long summary", body=self.driver.get_screenshot_as_png(),
                      attachment_type=AttachmentType.PNG)
        assert result.get("success") == False
        assert result.get("issue_key") is None
        assert result.get("error_in_field") == "summary"
        assert result.get("error_message") == "Summary must be less than 255 characters."

    @allure.epic('Jira WebUI')
    @allure.title('Test-UI-Issue-CRUD')
    @allure.description('Jira UI CRUD operations with issue')
    def test_create_update_issue(self, setup):
        assert self.login_page.login_to_jira() == True
        result = self.create_page.create_issue(project="AQAPYTHON", issue_type="Bug", summary="some_summary")
        allure.attach(name="Issue was just created", body=self.driver.get_screenshot_as_png(),
                      attachment_type=AttachmentType.PNG)
        assert result.get("success")
        self.issues["0"] = result.get("issue_key")
        assert self.issues.get("0") is not None
        self.issue_page.assign_issue_to_me(self.issues.get("0"))
        self.issue_page.update_priority(self.issues.get("0"), "High")
        self.issue_page.update_summary(self.issues.get("0"), "updated summary by isotnik")
        result = self.issue_filter_page.define_simple_filter(project="AQAPYTHON", issue_status="TO DO",
                                                             issue_type="Bug", search_text="updated summary by isotnik")
        allure.attach(name="Filtering issues by text", body=self.driver.get_screenshot_as_png(),
                      attachment_type=AttachmentType.PNG)
        assert result.get("total_results") == "1"

    @allure.epic('Jira WebUI')
    @allure.title('Test-UI-Issue-Filtering')
    @allure.description('Jira UI create issue with too long summary')
    def test_filter_issues(self, setup):
        assert self.login_page.login_to_jira() == True
        result = self.issue_filter_page.define_simple_filter(project="AQAPYTHON", search_text="some_summary by isotnik")
        assert result.get("total_results") == "0"

        assert self.rest_actions.authenticate().get("success")
        issue_fields = {'summary': 'some_summary by isotnik', 'description': 'item created via rest api'}
        result = self.rest_actions.createIssue("Story", issue_fields)
        assert result.get("status_code") == 201
        self.issues["0"] = result.get("issueKey")
        issue_fields = {'summary': 'some_summary by isotnik', 'description': 'item created via rest api'}
        result = self.rest_actions.createIssue("Story", issue_fields)
        assert result.get("status_code") == 201
        self.issues["1"] = result.get("issueKey")
        issue_fields = {'summary': 'some_summary by isotnik', 'description': 'item created via rest api'}
        result = self.rest_actions.createIssue("Bug", issue_fields)
        assert result.get("status_code") == 201
        self.issues["2"] = result.get("issueKey")
        issue_fields = {'summary': 'some_summary by isotnik', 'description': 'item created via rest api'}
        result = self.rest_actions.createIssue("Bug", issue_fields)
        assert result.get("status_code") == 201
        self.issues["3"] = result.get("issueKey")
        issue_fields = {'summary': 'some_summary by isotnik', 'description': 'item created via rest api'}
        result = self.rest_actions.createIssue("Bug", issue_fields)
        assert result.get("status_code") == 201
        self.issues["4"] = result.get("issueKey")

        result = self.issue_filter_page.define_simple_filter(project="AQAPYTHON", search_text="some_summary by isotnik")
        allure.attach(name="Filtering issues by text", body=self.driver.get_screenshot_as_png(),
                      attachment_type=AttachmentType.PNG)
        assert result.get("total_results") == "5"
        result = self.issue_filter_page.define_simple_filter(project="AQAPYTHON", search_text="some_summary by isotnik", issue_status="TO DO", issue_type="Bug")
        allure.attach(name="Filtering issues by text and issue type", body=self.driver.get_screenshot_as_png(),
                      attachment_type=AttachmentType.PNG)
        assert result.get("total_results") == "3"

