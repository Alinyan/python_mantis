from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.navigation import NavigationHelper
from fixture.page import PageHelper


class Application:
    def __init__(self, browser, baseURL):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        elif browser == "opera":
            self.wd = webdriver.Opera()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.navigation = NavigationHelper(self)
        self.page = PageHelper(self)
        self.baseURL = baseURL

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def destroy(self):
        self.wd.quit()

