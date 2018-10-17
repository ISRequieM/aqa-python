from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from pages.common import CommonObjects
from selenium import webdriver
import time
from jira.jira import JiraParameters


class IssuePage:
    page_url = "/browse/"

    ISSUE_BODY_DIV = (By.CSS_SELECTOR, "#issue-content div.issue-body-content")
    ASSIGN_TO_ME_LINK = (By.ID, "assign-to-me")
    SUMMARY_FIELD = (By.ID, "summary-val")
    SUMMARY_FIELD_INPUT = (By.CSS_SELECTOR, "#summary-val>#summary-form #summary")
    PRIORITY_FIELD = (By.ID, "priority-val")
    PRIORITY_FIELD_INPUT = (By.CSS_SELECTOR, "#priority-val #priority-form #priority-field")

    driver = None
    wait = None

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def go_to_issue(self, issue_key):
        self.driver.get(JiraParameters.url+self.page_url+issue_key)
        self.wait.until(expected_conditions.visibility_of_element_located(self.PRIORITY_FIELD))

    def assign_issue_to_me(self, issue_key):
        self.go_to_issue(issue_key)
        assign_to_me_link = self.wait.until(expected_conditions.element_to_be_clickable(self.ASSIGN_TO_ME_LINK))
        assign_to_me_link.click()

    def update_summary(self, issue_key, new_summary):
        self.go_to_issue(issue_key)
        summary_field = self.wait.until(expected_conditions.element_to_be_clickable(self.SUMMARY_FIELD))
        summary_field.click()
        summary_input = self.wait.until(expected_conditions.element_to_be_clickable(self.SUMMARY_FIELD_INPUT))
        summary_input.clear()
        summary_input.send_keys(new_summary)
        summary_input.send_keys(Keys.RETURN)

    def update_priority(self, issue_key, new_priority):
        self.go_to_issue(issue_key)
        priority_field = self.wait.until(expected_conditions.element_to_be_clickable(self.SUMMARY_FIELD))
        priority_field.click()
        priority_input = self.wait.until(expected_conditions.element_to_be_clickable(self.SUMMARY_FIELD_INPUT))
        priority_input.clear()
        priority_input.send_keys(new_priority)
        priority_input.send_keys(Keys.RETURN)


