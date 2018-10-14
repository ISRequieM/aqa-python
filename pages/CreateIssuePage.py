from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class CreateIssuePage:
    CREATE_BUTTON = (By.ID, "create_link")
    PROJECT_FIELD = (By.ID, "project-field")
    ISSUE_TYPE_FIELD = (By.ID, "issuetype-field")
    SUMMARY_FIELD = (By.ID, "summary")
    DESCRIPTION_FIELD = (By.ID, "tinymce")
    SUBMIT_ISSUE_BUTTON = (By.ID, "create-issue-submit")
    POPUP_CONTAINER = (By.ID, "aui-flag-container")

    driver = None
    wait = None

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def create_issue(self, project, issue_type, summary, description=None, priority=None, assignee=None):
        create_button = self.wait.until(expected_conditions.element_to_be_clickable(self.CREATE_BUTTON))
        create_button.click()
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
        popup_container = self.wait.until(expected_conditions.visibility_of_element_located(self.POPUP_CONTAINER))
        issue_key = popup_container.find_element(By.CLASS_NAME, "issue-created-key").get_attribute("data-issue-key")
        #self.wait.until(expected_conditions.invisibility_of_element(self.POPUP_CONTAINER)) #doesn't work in circle ci container
        return issue_key


