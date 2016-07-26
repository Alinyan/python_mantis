
class NavigationHelper:

    def __init__(self, app):
        self.app = app

    def open_start_page(self):
        self.app.wd.get(self.app.baseURL)

    def open_manage_project_page(self):
        self.app.wd.find_element_by_link_text("Manage").click()
        self.app.wd.find_element_by_link_text("Manage Projects").click()
