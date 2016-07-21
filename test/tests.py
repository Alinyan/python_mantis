from model.project import Project
import random


def test_add_project(db, app, json_projects):
    old_list_projects = db.get_list_projects()
    app.project.create(json_projects)
    new_list_projects = db.get_list_projects()
    old_list_projects.append(json_projects)
    assert sorted(new_list_projects, key=Project.id_or_max) == sorted(old_list_projects, key=Project.id_or_max)


def test_delete_project(db, app, json_projects):
    if len(db.get_list_projects()) == 0:
        app.project.create(json_projects)
    old_list_projects = db.get_list_projects()
    project = random.choice(old_list_projects)
    app.project.delete_by_id(project.id)
    new_list_projects = db.get_list_projects()
    old_list_projects.remove(project)
    assert sorted(new_list_projects, key=Project.id_or_max) == sorted(old_list_projects, key=Project.id_or_max)