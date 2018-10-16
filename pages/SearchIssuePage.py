from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
import time
from jira.jira import JiraParameters


class SearchIssuePage:
    page_url = "/issues/?jql="
    CRITERIA_PROJECT_BUTTON = (By.CSS_SELECTOR, "ul.criteria-list>li[data-id='project']>button[data-id='project']")
    CRITERIA_PROJECT_INPUT = (By.CSS_SELECTOR, "#issue-filter #searcher-pid-input")
    CRITERIA_TYPE_BUTTON = (By.CSS_SELECTOR, "ul.criteria-list>li[data-id='issuetype']>button[data-id='issuetype']")
    CRITERIA_TYPE_INPUT = (By.CSS_SELECTOR, "#issue-filter #searcher-type-input")
    CRITERIA_STATUS_BUTTON = (By.CSS_SELECTOR, "ul.criteria-list>li[data-id='status']>button[data-id='status']")
    CRITERIA_STATUS_INPUT = (By.CSS_SELECTOR, "#issue-filter #searcher-status-input")
    CRITERIA_ASSIGNEE_BUTTON = (By.CSS_SELECTOR, "ul.criteria-list>li[data-id='assignee']>button[data-id='assignee']")
    CRITERIA_ASSIGNEE_INPUT = (By.CSS_SELECTOR, "#issue-filter #assignee-input")
    CRITERIA_TEXT_INPUT = (By.ID, "searcher-query")
    ISSUE_TABLE = (By.ID, "issuetable")
    ISSUE_TABLE_ROWS = (By.CSS_SELECTOR, "#issuetable>tbody.ui-sortable>tr")
    TOTAL_NUMBER_ISSUES_FOUND = (By.CSS_SELECTOR, "div.list-view>div.issue-table-info-bar span.results-count-total")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "div.empty-results>div.no-results-message>h3")
    TABLE_PENDING_STATE = (By.CSS_SELECTOR, "div.pending")


    driver = None
    wait = None

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def go_to_page(self):
        self.driver.get(JiraParameters.url+self.page_url)
        self.wait.until(expected_conditions.element_to_be_clickable(self.CRITERIA_PROJECT_BUTTON))

    def wait_table_refreshed(self):
        self.wait.until(expected_conditions.invisibility_of_element_located(self.TABLE_PENDING_STATE))

    def define_simple_filter(self, project=None, issue_type=None, issue_status=None, assignee=None, search_text=None ):
        self.go_to_page()
        if project is not None:
            button_project = self.wait.until(expected_conditions.element_to_be_clickable(self.CRITERIA_PROJECT_BUTTON))
            button_project.click()
            input_project = self.wait.until(expected_conditions.element_to_be_clickable(self.CRITERIA_PROJECT_INPUT))
            input_project.send_keys(project)
            input_project.send_keys(Keys.RETURN)
            self.wait_table_refreshed()
            button_project.click()
            self.wait.until(expected_conditions.invisibility_of_element_located(self.CRITERIA_PROJECT_INPUT))
        if issue_status is not None:
            button_issue_type = self.wait.until(expected_conditions.element_to_be_clickable(self.CRITERIA_TYPE_BUTTON))
            button_issue_type.click()
            input_issue_type = self.wait.until(expected_conditions.element_to_be_clickable(self.CRITERIA_TYPE_INPUT))
            input_issue_type.send_keys(issue_type)
            input_issue_type.send_keys(Keys.RETURN)
            self.wait_table_refreshed()
            button_issue_type.click()
            self.wait.until(expected_conditions.invisibility_of_element_located(self.CRITERIA_TYPE_INPUT))
        if issue_status is not None:
            button_issue_status = self.wait.until(expected_conditions.element_to_be_clickable(self.CRITERIA_STATUS_BUTTON))
            button_issue_status.click()
            input_issue_status = self.wait.until(expected_conditions.element_to_be_clickable(self.CRITERIA_STATUS_INPUT))
            input_issue_status.send_keys(issue_status)
            input_issue_status.send_keys(Keys.RETURN)
            self.wait_table_refreshed()
            button_issue_status.click()
            self.wait.until(expected_conditions.invisibility_of_element_located(self.CRITERIA_STATUS_INPUT))
        if assignee is not None:
            button_assignee = self.wait.until(expected_conditions.element_to_be_clickable(self.CRITERIA_ASSIGNEE_BUTTON))
            button_assignee.click()
            input_assignee = self.wait.until(expected_conditions.element_to_be_clickable(self.CRITERIA_ASSIGNEE_INPUT))
            input_assignee.send_keys(assignee)
            input_assignee.send_keys(Keys.RETURN)
            self.wait_table_refreshed()
            button_assignee.click()
            self.wait.until(expected_conditions.invisibility_of_element_located(self.CRITERIA_ASSIGNEE_INPUT))
        if search_text is not None:
            text_input = self.wait.until(expected_conditions.element_to_be_clickable(self.CRITERIA_TEXT_INPUT))
            text_input.send_keys(search_text)
            text_input.send_keys(Keys.RETURN)
            self.wait_table_refreshed()
        try:
            WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.TOTAL_NUMBER_ISSUES_FOUND))
        except StaleElementReferenceException:
            self.wait.until(expected_conditions.visibility_of_element_located(self.NO_RESULTS_MESSAGE))
            return {"total_results": "0"}
        except TimeoutException:
            self.wait.until(expected_conditions.visibility_of_element_located(self.NO_RESULTS_MESSAGE))
            return {"total_results": "0"}
        total_results = (self.wait.until(expected_conditions.visibility_of_element_located(self.TOTAL_NUMBER_ISSUES_FOUND))).text
        return {"total_results": total_results}
