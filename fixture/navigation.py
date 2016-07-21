
class NavigationHelper:

    def __init__(self, app):
        self.app = app

    def open_start_page(self):
        self.app.wd.get(self.app.baseURL)

    def open_manage_project_page(self):
        self.app.wd.find_element_by_link_text("Manage").click()
        self.app.wd.find_element_by_link_text("Manage Projects").click()

    def go_to_group_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("group.php") and len(wd.find_elements_by_name("new")) > 0):
            self.app.wd.find_element_by_link_text("groups").click()

    def go_to_edit_contact_page_by_index(self, index):
        self.select_contact_by_index(index)
        # submit to edit
        self.app.wd.find_element_by_xpath(
            "//table/tbody/tr[%s]/td[8]/a/img" % str(index + 2)).click()

    def go_to_edit_contact_page_by_id(self, id):
        self.select_contact_by_id(id)
        # submit to edit
        self.app.wd.find_element_by_css_selector(
            "a[href='edit.php?id=%s']" % id).click()

    def go_to_view_contact_page(self, index):
        self.select_contact_by_index(index)
        # submit to view details
        self.app.wd.find_element_by_xpath(
            "//table/tbody/tr[%s]/td[7]/a/img" % str(index + 2)).click()

    def select_contact_by_index(self, index):
        self.go_to_home_page()
        self.app.wd.find_elements_by_name("selected[]")[index].click()

    def select_contact_by_id(self, id):
        self.go_to_home_page()
        self.app.wd.find_element_by_css_selector("input[id='%s']" % id).click()
