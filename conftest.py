import pytest
import os.path
import json
import importlib
import jsonpickle
import ftputil
from fixture.application import Application
from fixture.orm import ORMFixture

fixture = None
conf = None

def load_config(file):
    global conf
    if conf is None:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file)) as json_file:
            conf = json.load(json_file)
    return conf

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--config"))

@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    fixture.session.ensure_login(username=config['web']["username"], password=config['web']["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)

def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile('config_inc.php'):
            remote.rename('config_inc.php', 'config_inc.php.bak')
        remote.upload(os.path.join(os.path.dirname(__file__), 'resources/config_inc.php'), 'config_inc.php' )

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile('config_inc.php'):
                remote.remove("config_inc.php")
            remote.rename('config_inc.php.bak', 'config_inc.php')

@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def exit():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(exit)
    return fixture

@pytest.fixture(scope="session")
def db(request):
    db_conf = load_config(request.config.getoption("--config"))['db']
    dbfixture = ORMFixture(host=db_conf['host'], name=db_conf['name'], user=db_conf['user'], password=db_conf['password'])
    return dbfixture

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--config", action="store", default="config.json")

def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])

def load_from_module(module):
    return importlib.import_module("data.%s" % module).constant_data

def load_from_json(json):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % json)) as file:
        return jsonpickle.decode(file.read())
