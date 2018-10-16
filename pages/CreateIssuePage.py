from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from pages.common import CommonObjects


class CreateIssuePage:
    CREATE_BUTTON = (By.ID, "create_link")
    PROJECT_FIELD = (By.ID, "project-field")
    ISSUE_TYPE_FIELD = (By.ID, "issuetype-field")
    SUMMARY_FIELD = (By.ID, "summary")
    DESCRIPTION_FIELD = (By.ID, "tinymce")
    SUBMIT_ISSUE_BUTTON = (By.ID, "create-issue-submit")
    SUCCESS_POPUP_CONTAINER = (By.CSS_SELECTOR, "#aui-flag-container div.aui-message-success")
    CREATE_DIALOG = (By.ID, "create-issue-dialog")
    return_result = {"success": None, "error_message": None, "error_in_field": None, "issue_key": None}

    driver = None
    wait = None
    common_objects = None

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.common_objects = CommonObjects(self.driver)

    def create_issue(self, project, issue_type, summary, description=None, priority=None, assignee=None):
        self.common_objects.close_timezone_popup()
        create_button = self.wait.until(expected_conditions.element_to_be_clickable(self.CREATE_BUTTON))
        create_button.click()
        self.wait.until(expected_conditions.presence_of_element_located(self.CREATE_DIALOG))
        project_field = self.wait.until(expected_conditions.element_to_be_clickable(self.PROJECT_FIELD))
        project_field.clear()
        project_field.send_keys(project)
        project_field.send_keys(Keys.RETURN)
        issue_type_field = self.wait.until(expected_conditions.element_to_be_clickable(self.ISSUE_TYPE_FIELD))
        issue_type_field.clear()
        issue_type_field.send_keys(issue_type)
        issue_type_field.send_keys(Keys.RETURN)
        summary_field = self.wait.until(expected_conditions.element_to_be_clickable(self.SUMMARY_FIELD))
        summary_field.clear()
        summary_field.send_keys(summary)
        submit_issue_button = self.wait.until(expected_conditions.element_to_be_clickable(self.SUBMIT_ISSUE_BUTTON))
        submit_issue_button.click()
        self.wait.until_not(expected_conditions.invisibility_of_element(self.CREATE_DIALOG))
        try:
            popup_container = self.wait.until(expected_conditions.visibility_of_element_located(self.SUCCESS_POPUP_CONTAINER))
        except TimeoutException:
            print("Failed to post issue")
            error = self.wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#create-issue-dialog div.error")))
            self.return_result["error_in_field"] = error.get_attribute("data-field")
            self.return_result["error_message"] = error.text
            self.return_result["success"] = False
            return self.return_result
        #popup_container = self.driver.find_element(self.POPUP_CONTAINER)
        issue_key = popup_container.find_element(By.CLASS_NAME, "issue-created-key").get_attribute("data-issue-key")
        #self.wait.until(expected_conditions.invisibility_of_element(self.POPUP_CONTAINER)) #doesn't work in circle ci container
        self.return_result["success"] = True
        self.return_result["issue_key"] = issue_key
        return self.return_result


