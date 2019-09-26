import shutil
from pathlib import Path

import sh
import pytest


@pytest.fixture
def result(tmpdir, request):
    dir_ = Path(request.fspath).parent
    tdir = Path(tmpdir)
    workdir = shutil.copytree(dir_, tdir / "case")
    try:
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
