from pony.orm import *
from datetime import datetime
from model.project import Project
from pymysql.converters import decoders


class ORMFixture:

    db = Database()

    class ORMProject(db.Entity):
        _table_ = 'mantis_project_table'
        id =PrimaryKey(int, column='id')
        name = Optional(str, column='name')
        description = Optional(str, column='description')

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password, conv=decoders)
        self.db.generate_mapping()
        sql_debug(True)

    def convert_projects_to_model(self, projects):
        def convert(project):
            return Project(id=str(project.id), name=project.name, description=project.description)
        return list(map(convert, projects))

    @db_session
    def get_list_projects(self):
        return self.convert_projects_to_model(select(g for g in ORMFixture.ORMProject))

    @db_session
    def get_contacts_not_in_group_by_id(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model\
            (select(c for c in ORMFixture.ORMContact if c.deprecated is None and orm_group not in c.groups))

    @db_session
    def get_contacts_in_group_by_name(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.name == group.name))[0]
        return self.convert_contacts_to_model(orm_group.contacts)

    @db_session
    def get_contacts_not_in_group_by_name(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.name == group.name))[0]
        return self.convert_contacts_to_model\
            (select(c for c in ORMFixture.ORMContact if c.deprecated is None and orm_group not in c.groups))

