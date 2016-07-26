from model.project import Project
import random
import string

def random_string(prefix, maxlen):
    char = string.ascii_letters + string.hexdigits + ' '*5 #+ string.punctuation
    return prefix + "".join([random.choice(char) for i in range(random.randrange(maxlen))])

random_data = Project(name=random_string("name", 20), description=random_string("description", 20))

def test_add_project(app):
    old_list_projects = app.soap.get_list_projects()
    app.project.create(random_data)
    new_list_projects = app.soap.get_list_projects()
    old_list_projects.append(random_data)
    assert sorted(new_list_projects, key=Project.id_or_max) == sorted(old_list_projects, key=Project.id_or_max)

def test_delete_project(app):
    if len(app.soap.get_list_projects()) == 0:
        app.project.create(random_data)
    old_list_projects = app.soap.get_list_projects()
    project = random.choice(old_list_projects)
    app.project.delete_by_id(project.id)
    new_list_projects = app.soap.get_list_projects()
    old_list_projects.remove(project)
    assert sorted(new_list_projects, key=Project.id_or_max) == sorted(old_list_projects, key=Project.id_or_max)