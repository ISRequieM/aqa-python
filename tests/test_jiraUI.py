import time

import pytest
from webdriver_manager.chrome import ChromeDriverManager

from jira.jira import JiraParameters
from pages.CreateIssuePage import CreateIssuePage
from pages.LoginPage import LoginPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jira.jira import JiraRestActions
from pages.SearchIssuePage import SearchIssuePage


class Test_JiraUI:
    driver = None
    login_page = None
    create_page = None
    issue_key = None
    rest_actions = None
    issue_filter_page = None

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
        self.login_page = LoginPage(self.driver)
        self.create_page = CreateIssuePage(self.driver)
        self.issue_filter_page = SearchIssuePage(self.driver)
        user = JiraParameters.user
        password = JiraParameters.password
        project_key = JiraParameters.project_key
        self.rest_actions = JiraRestActions(user, password, project_key)

        def fin():
            print("\nPerforming tear down")
            self.driver.quit()
            if self.issue_key is not None:
                assert self.rest_actions.authenticate() != "Failed"
                assert self.rest_actions.delete_issue(self.issue_key).get("success")

        request.addfinalizer(fin)
        print("\nSetup was performed")

    def test_jira_login_wrong_password(self, setup):
        assert self.login_page.login_to_jira_creds_privided(JiraParameters.user, "admin") == False

    def test_jira_login_wrong_username(self, setup):
        assert self.login_page.login_to_jira_creds_privided("admin", JiraParameters.password) == False

    def test_create_issue_missing_summary(self, setup):
        assert self.login_page.login_to_jira() == True
        result = self.create_page.create_issue(project="AQAPYTHON", issue_type="Bug", summary="")
        assert result.get("success") == False
        assert result.get("issue_key") is None
        assert result.get("error_in_field") == "summary"
        assert result.get("error_message") == "You must specify a summary of the issue."

    def test_create_issue_too_long_summary(self, setup):
        assert self.login_page.login_to_jira() == True
        summary = 'some_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarys'+\
                            'ome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysom'+\
                            'e_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_s'+\
                            'ummarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summa'+\
                            'rysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome'+\
                            '_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summary'+\
                            'some_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summary'
        result = self.create_page.create_issue(project="AQAPYTHON", issue_type="Bug", summary=summary)
        assert result.get("success") == False
        assert result.get("issue_key") is None
        assert result.get("error_in_field") == "summary"
        assert result.get("error_message") == "Summary must be less than 255 characters."

    def test_create_issue(self, setup):
        assert self.login_page.login_to_jira() == True
        result = self.create_page.create_issue(project="AQAPYTHON", issue_type="Bug", summary="some_summary")
        assert result.get("success")
        self.issue_key = result.get("issue_key")
        assert self.issue_key is not None
        print("\n" + self.issue_key)
        result = self.issue_filter_page.define_simple_filter(project="AQAPYTHON", issue_status="TO DO",
                                                             issue_type="Bug", search_text="some_summary")
        assert result.get("total_results") == "1"



    def test_issue_filter(self, setup):
        assert self.login_page.login_to_jira() == True
        result = self.issue_filter_page.define_simple_filter(project="AQAPYTHON", issue_status="TO DO",
                                                             issue_type="Bug", search_text="some_summary")
        assert result.get("total_results") == "0"

