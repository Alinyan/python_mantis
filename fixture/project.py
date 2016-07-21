# -*- coding: utf-8 -*-
from selenium.webdriver.support.select import Select
import random

class ProjectHelper:

    project_cache = None

    def __init__(self, app):
        self.app = app

    def create(self, project):
        self.app.navigation.open_manage_project_page()
        # init project creation
        self.app.wd.find_element_by_xpath("//*[@value='Create New Project']").click()
        # fill project form
        self.app.page.fill_field(name="name", value=project.name)
        index = random.randrange(len(self.app.wd.find_elements_by_xpath("//select[@name='status']/option")))
        Select(self.app.wd.find_element_by_xpath("//select[@name='status']")).select_by_index(index)
        index = random.randrange(len(self.app.wd.find_elements_by_xpath("//select[@name='view_state']/option")))
        Select(self.app.wd.find_element_by_xpath("//select[@name='view_state']")).select_by_index(index)
        self.app.page.fill_field(name="description", value=project.description)
        # Enter project creation
        self.app.wd.find_element_by_xpath("//*[@value='Add Project']").click()
        self.app.navigation.open_manage_project_page()
        self.project_cache = None

    def delete_by_id(self, id):
        self.app.navigation.open_manage_project_page()
        # select project by id
        self.app.wd.find_element_by_xpath("//a[@href='manage_proj_edit_page.php?project_id=%s']" % id).click()
        # confirm deletion
        self.app.wd.find_element_by_xpath("//*[@value='Delete Project']").click()
        self.app.wd.find_element_by_xpath("//*[@value='Delete Project']").click()
        self.app.navigation.open_manage_project_page()
        self.contact_cache = None