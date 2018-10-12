from webdriver_manager.chrome import ChromeDriverManager
from pages.LoginPage import LoginPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestJiraLogin:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    login_page = LoginPage(driver)

    def test_jira_login(self):
        assert self.login_page.login_to_jira()

    def test_cleanup(self):
        self.driver.quit()


