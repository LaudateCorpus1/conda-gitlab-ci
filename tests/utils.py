import os
import subprocess

from conda_build.conda_interface import Resolve
import networkx as nx
import pytest


@pytest.fixture(scope='function')
def testing_workdir(tmpdir, request):
    """ Create a workdir in a safe temporary folder; cd into dir above before test, cd out after

    :param tmpdir: py.test fixture, will be injected
    :param request: py.test fixture-related, will be injected (see pytest docs)
    """

    saved_path = os.getcwd()

    tmpdir.chdir()
    # temporary folder for profiling output, if any
    tmpdir.mkdir('prof')

    def return_to_saved_path():
        if os.path.isdir(os.path.join(saved_path, 'prof')):
            profdir = tmpdir.join('prof')
            files = profdir.listdir('*.prof') if profdir.isdir() else []

            for f in files:
                f.rename(os.path.join(saved_path, 'prof', f.basename))
        os.chdir(saved_path)

    request.addfinalizer(return_to_saved_path)

    return str(tmpdir)


@pytest.fixture(scope='function')
def testing_git_repo(testing_workdir, request):
    subprocess.check_call(['git', 'init'])
    with open('sample_file', 'w') as f:
        f.write('weee')
    subprocess.check_call(['git', 'add', 'sample_file'])
    subprocess.check_call(['git', 'commit', '-m', 'commit 1'])
    os.makedirs('test_dir_1')
    os.makedirs('not_a_recipe')
    with open(os.path.join('test_dir_1', 'meta.yaml'), 'w') as f:
        # not valid meta.yaml.  Doesn't matter for test.
        f.write('weee')
    with open(os.path.join('not_a_recipe', 'testfile'), 'w') as f:
        f.write('weee')
    subprocess.check_call(['git', 'add', 'test_dir_1'])
    subprocess.check_call(['git', 'commit', '-m', 'commit 2'])
    os.makedirs('test_dir_2')
    with open(os.path.join('test_dir_2', 'meta.yaml'), 'w') as f:
        f.write('weee')
    subprocess.check_call(['git', 'add', 'test_dir_2'])
    subprocess.check_call(['git', 'commit', '-m', 'commit 3'])
    return request


@pytest.fixture(scope='function')
def testing_graph(request):
    g = nx.DiGraph()
    for x in ['a', 'b', 'c', 'd']:
        g.add_node(x, version="1.0", build="0")
    g.add_edge('a', 'b')
    g.add_edge('b', 'c')
    g.add_edge('c', 'd')
    g.node['b']['dirty'] = True
    g.node['b']['meta'] = 'something'
    return g


@pytest.fixture(scope='function')
def testing_conda_resolve(request):
    index = {
        "a": {
            "build": "0",
            "build_number": 0,
            "date": "2015-10-28",
            "depends": [],
            "license": "LGPL",
            "md5": "7268f7dcc075e615af758d1243ed4f1d",
            "name": "a",
            "requires": [],
            "size": 303694,
            "version": "920"
        },
        "b": {
            "build": "0",
            "build_number": 0,
            "date": "2015-10-28",
            "depends": [],
            "license": "LGPL",
            "md5": "7268f7dcc075e615af758d1243ed4f1d",
            "name": "b",
            "requires": [],
            "size": 303694,
            "version": "920"
        },
        "c": {
            "build": "0",
            "build_number": 0,
            "date": "2015-10-28",
            "depends": [],
            "license": "LGPL",
            "md5": "7268f7dcc075e615af758d1243ed4f1d",
            "name": "c",
            "requires": [],
            "size": 303694,
            "version": "920"
        },
        "d": {
            "build": "0",
            "build_number": 0,
            "date": "2015-10-28",
            "depends": [],
            "license": "LGPL",
            "md5": "7268f7dcc075e615af758d1243ed4f1d",
            "name": "d",
            "requires": [],
            "size": 303694,
            "version": "920"
        }
    }
    return Resolve(index)
