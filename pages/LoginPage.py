from selenium.webdriver.common.by import By
from jira.jira import JiraParameters
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

class LoginPage:
    login_url = "/login.jsp"
    USER_INPUT = (By.ID, "login-form-username")
    PASSWORD_INPUT = (By.ID, "login-form-password")
    LOGIN_BUTTON = (By.ID, "login-form-submit")
    CREATE_BUTTON = (By.ID, "create_link")
    USER_HEADER = (By.ID, "header-details-user-fullname")
    driver_instance = None
    user = None
    password = None
    wait = None

    def __init__(self, driver):
        self.driver_instance = driver
        self.user = JiraParameters.user
        self.password = JiraParameters.password
        self.wait = WebDriverWait(driver=self.driver_instance, timeout=int(10))

    def login_to_jira(self):
        self.driver_instance.get(JiraParameters.url+self.login_url)
        login_button = self.wait.until(expected_conditions.element_to_be_clickable(self.LOGIN_BUTTON))
        self.driver_instance.find_element(*self.USER_INPUT).send_keys(*self.user)
        self.driver_instance.find_element(*self.PASSWORD_INPUT).send_keys(*self.password)
        login_button.click()
        try:
            self.wait.until(expected_conditions.visibility_of_element_located(self.USER_HEADER))
            return True
        except TimeoutException:
            return False

    def login_to_jira_creds_privided(self, user, password):
        self.driver_instance.get(JiraParameters.url+self.login_url)
        login_button = self.wait.until(expected_conditions.visibility_of_element_located(self.LOGIN_BUTTON))
        self.driver_instance.find_element(*self.USER_INPUT).send_keys(user)
        self.driver_instance.find_element(*self.PASSWORD_INPUT).send_keys(password)
        login_button.click()
        try:
            self.wait.until(expected_conditions.visibility_of_element_located(self.USER_HEADER))
            return True
        except TimeoutException:
            return False



