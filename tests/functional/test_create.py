import os
import sys

import pytest
import scripttest


IS_WINDOWS = (
    sys.platform.startswith("win") or
    (sys.platform == "cli" and os.name == "nt")
)
IS_26 = sys.version_info[:2] == (2, 6)
PYTHON_BINS = [
    "C:\\Python27\\python.exe",
    "C:\\Python27-x64\\python.exe",
    "C:\\Python33\\python.exe",
    "C:\\Python33-x64\\python.exe",
    "C:\\Python34\\python.exe",
    "C:\\Python34-x64\\python.exe",
    "C:\\PyPy\\pypy.exe",
    "C:\\PyPy3\\pypy.exe",
    None,
    "python",
    "python2.6",
    "python2.7",
    "python3.2",
    "python3.3",
    "python3.4",
    "pypy",
]


@pytest.yield_fixture
def env(request):
    env = scripttest.TestFileEnvironment()
    try:
        yield env
    finally:
        env.clear()


@pytest.yield_fixture(params=PYTHON_BINS)
def python(request):
    if request.param is None or os.path.exists(request.param):
        yield request.param
    else:
        pytest.skip(msg="Implementation at %r not available." % request.param)


def test_create_via_script(env, python):
    extra = ['--python', python] if python else []
    result = env.run('virtualenv', 'myenv', *extra)
    if IS_WINDOWS:
        assert 'myenv\\Scripts\\activate.bat' in result.files_created
        assert 'myenv\\Scripts\\activate.ps1' in result.files_created
        assert 'myenv\\Scripts\\activate_this.py' in result.files_created
        assert 'myenv\\Scripts\\deactivate.bat' in result.files_created
        assert 'myenv\\Scripts\\pip.exe' in result.files_created
        assert 'myenv\\Scripts\\python.exe' in result.files_created
    else:
        assert 'myenv/bin/activate.sh' in result.files_created
        assert 'myenv/bin/activate_this.py' in result.files_created
        assert 'myenv/bin/python' in result.files_created


def test_create_via_module(env, python):
    extra = ['--python', python] if python else []
    result = env.run('python', '-mvirtualenv.__main__' if IS_26 else '-mvirtualenv', 'myenv', *extra)
    if IS_WINDOWS:
        assert 'myenv\\Scripts\\activate.bat' in result.files_created
        assert 'myenv\\Scripts\\activate.ps1' in result.files_created
        assert 'myenv\\Scripts\\activate_this.py' in result.files_created
        assert 'myenv\\Scripts\\deactivate.bat' in result.files_created
        assert 'myenv\\Scripts\\pip.exe' in result.files_created
        assert 'myenv\\Scripts\\python.exe' in result.files_created
    else:
        assert 'myenv/bin/activate.sh' in result.files_created
        assert 'myenv/bin/activate_this.py' in result.files_created
        assert 'myenv/bin/python' in result.files_created
