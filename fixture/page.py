
class PageHelper:

    def __init__(self, app):
        self.app = app

    def fill_field(self, name, value):
        if value is not None:
            self.app.wd.find_element_by_name(name).click()
            self.app.wd.find_element_by_name(name).clear()
            self.app.wd.find_element_by_name(name).send_keys(value)

