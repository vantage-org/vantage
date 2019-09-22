import os
from pathlib import Path

from click.testing import CliRunner
from vantage.entry import vantage


def test_nothing_provided_uses_cwd():
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        result = runner.invoke(vantage, ["env"])
        assert result.exit_code == 0
        lines = result.output.splitlines()
        # Need to resolve() to fix quirk in macOS with /var/ vs /private/var/
        path = Path(fs).resolve()
        assert f"VG_APP_DIR={path}" in lines


def test_specified():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(vantage, ["--app", "/tmp", "env"])
        assert result.exit_code == 0
        lines = result.output.splitlines()
        # Need to resolve() to fix quirk in macOS with /tmp/ vs /private/tmp/
        path = Path("/tmp").resolve()
        assert f"VG_APP_DIR={path}" in lines


def test_nothing_provided_uses_first_parent_with_vg_file():
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        with open(".vantage", "w") as f:
            f.write("")
        sub_dir = Path(fs) / "sub_dir"
        sub_dir.mkdir()
        os.chdir(sub_dir)

        result = runner.invoke(vantage, ["env"])
        assert result.exit_code == 0
        lines = result.output.splitlines()
        # Need to resolve() to fix quirk in macOS with /var/ vs /private/var/
        path = Path(fs).resolve()
        assert f"VG_APP_DIR={path}" in lines
