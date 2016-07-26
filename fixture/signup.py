
import re

class SignupHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, username, email,  password):
        self.app.wd.get(self.app.baseURL + '/signup_page.php')
        self.app.wd.find_element_by_name('username').send_keys(username)
        self.app.wd.find_element_by_name('email').send_keys(email)
        self.app.wd.find_element_by_xpath("//input[@value='Signup']").click()

        mail = self.app.mail.get_mail(username, password, "[MantisBT] Account registration")
        url = self.extract_confirmation_url(mail)

        self.app.wd.get(url)
        self.app.wd.find_element_by_name('password').send_keys(password)
        self.app.wd.find_element_by_name('password_confirm').send_keys(password)
        self.app.wd.find_element_by_css_selector("input[value='Update User']").click()


    def extract_confirmation_url(self, text):
        return re.search("http://.*$", text, re.M).group(0)



