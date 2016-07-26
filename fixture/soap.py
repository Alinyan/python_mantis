from model.project import Project
from suds.client import Client
from suds import WebFault

class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.19/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False


    def get_list_projects(self):
        username = self.app.config['web']['username']
        password =self.app.config['web']['password']
        client = Client("http://localhost/mantisbt-1.2.19/api/soap/mantisconnect.php?wsdl")
        list_contacts = []
        for project in client.service.mc_projects_get_user_accessible(username, password):
            list_contacts.append(Project(id=str(project.id), name=str(project.name), description=str(project.description)))
        return list_contacts
