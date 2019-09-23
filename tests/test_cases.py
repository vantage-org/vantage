import shlex
from pathlib import Path

import sh


def test_case(tmpdir, case):
    tmpdir = Path(tmpdir).resolve()
    _cwd = tmpdir
    if "pre" in case:
        pre = case["pre"]
        if "cwd" in pre:
            _cwd = tmpdir / pre["cwd"]
            _cwd.mkdir(parents=True)
        for path, contents in pre.get("files", {}).items():
            path = tmpdir / path
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w") as fp:
                fp.write("\n".join(contents))

    cmd = sh.Command("./dist/vantage")
    try:
        kwargs = {"_cwd": _cwd}
        if "stdin" in case:
            kwargs["_in"] = case["stdin"]
        res = cmd(shlex.split(case.get("invoke", "")), **kwargs)
    except sh.ErrorReturnCode as erc:
        res = erc

    if "post" in case:
        post = case["post"]
        if "code" in post:
            assert res.exit_code == post["code"]
        if "stdout" in post:
            wanted = {
                line.strip().replace("$BASE", str(tmpdir)) for line in post["stdout"]
            }
            actual = res.stdout.decode("utf-8").strip().splitlines()
            assert wanted <= {*actual}
        if "stderr" in post:
            wanted = {
                line.strip().replace("$BASE", str(tmpdir)) for line in post["stderr"]
            }
            actual = res.stderr.decode("utf-8").strip().splitlines()
            assert wanted <= {*actual}
        for path, contents in post.get("files", {}).items():
            path = tmpdir / path
            assert path.is_file()
            with path.open("r") as fp:
                actual = {line.strip() for line in fp}
                assert {*contents} <= actual
