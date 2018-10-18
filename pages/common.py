from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException
from selenium import webdriver
import time
from jira.jira import JiraParameters

class CommonObjects:
    TIMEZONE_POPUP = (By.CSS_SELECTOR, "#aui-flag-container div.aui-message-info.closeable.shadowed")
    TIMEZONE_POPUP_CLOSE = (By.CSS_SELECTOR, "#aui-flag-container div.aui-message-info.closeable.shadowed>span[role='button']")
    BUSY_ANNIMATION_SPINNER = (By.CSS_SELECTOR, "div.spinner")

    driver = None
    wait = None

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 7)

    def close_timezone_popup(self):
        try:
            self.wait.until(expected_conditions.visibility_of_element_located(self.TIMEZONE_POPUP))
            (self.wait.until(expected_conditions.element_to_be_clickable(self.TIMEZONE_POPUP_CLOSE))).click()
            self.wait.until(expected_conditions.invisibility_of_element_located(self.TIMEZONE_POPUP))
        except WebDriverException:
            print("\n No timezone popup was shown actually")

    def wait_until_busy_spinner_hidden(self):
        WebDriverWait(self.driver, 20).until(expected_conditions.invisibility_of_element_located(self.BUSY_ANNIMATION_SPINNER))




