import shutil
from pathlib import Path

import sh
import pytest


@pytest.fixture
def workdir(tmpdir, request):
    dir_ = Path(request.fspath).parent
    tdir = Path(tmpdir)
    return shutil.copytree(dir_, tdir / "case")


@pytest.fixture
def run(workdir, request):

    def wrapper():
        test_name = Path(request.fspath).stem.replace("test_", "")
        try:
            path = Path(workdir) / f"{test_name}.sh"
            if path.is_file():
                res = sh.sh(str(path), _cwd=workdir)
            else:
                res = sh.sh(f"{workdir}/run.sh", _cwd=workdir)
        except sh.ErrorReturnCode as erc:
            res = erc
        res.stdout_ = res.stdout.decode("utf-8").strip()
        res.stderr_ = res.stderr.decode("utf-8").strip()
        return res

    return wrapper


@pytest.fixture
def result(run):
    return run()


@pytest.fixture
def stdout(result):
    return result.stdout_


@pytest.fixture
def stderr(result):
    return result.stderr_


@pytest.fixture
def get_file(tmpdir):

    def getter(path):
        f = Path(tmpdir) / "case" / path
        return f.read_text().strip()

    return getter
