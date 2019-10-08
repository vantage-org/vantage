import shutil
from pathlib import Path

import sh
import pytest


@pytest.fixture
def result(tmpdir, request):
    dir_ = Path(request.fspath).parent
    test_name = Path(request.fspath).stem.replace("test_", "")
    tdir = Path(tmpdir)
    workdir = shutil.copytree(dir_, tdir / "case")
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


@pytest.fixture
def get_file(tmpdir):

    def getter(path):
        f = Path(tmpdir) / "case" / path
        return f.read_text().strip()

    return getter
