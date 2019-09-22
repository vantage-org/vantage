import pytest
from click.testing import CliRunner

from vantage.entry import vantage


def test_no_args():
    runner = CliRunner()
    result = runner.invoke(vantage, ["--var", "FOO=BAR", "__env"])
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert "FOO=BAR" in lines


def test_no_args_with_base64_value():
    runner = CliRunner()
    result = runner.invoke(vantage, ["--var", "FOO=base64:QkFS", "__env"])
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert "FOO=BAR" in lines


def test_get_value():
    runner = CliRunner()
    result = runner.invoke(vantage, ["--var", "FOO=BAR", "__env", "FOO"])
    assert result.exit_code == 0
    assert result.output == "BAR\n"


def test_get_value_for_missing_key():
    runner = CliRunner()
    result = runner.invoke(vantage, ["__env", "FOO"])
    assert result.exit_code == 1
    assert result.output == "Error: No value found for 'FOO'\n"


def test_get_base64value():
    runner = CliRunner()
    result = runner.invoke(vantage, ["--var", "FOO=base64:QkFS", "__env", "FOO"])
    assert result.exit_code == 0
    assert result.output == "BAR\n"


def test_set_value():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(vantage, ["--env", "test", "__env", "FOO=BAR"])
        assert result.exit_code == 0
        assert result.output == ""
        with open("test", "r") as fp:
            contents = fp.read().strip()
            assert contents == "FOO=BAR"


@pytest.mark.xfail()
def test_set_value_from_stdin():
    # invoke's input args fakes the input from stdin in a way that the __env
    # command doesn't detect.
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            vantage, ["--env", "test", "__env", "FOO"], input="BAR\n"
        )
        assert result.exit_code == 0
        assert result.output == ""
        with open("test", "r") as fp:
            contents = fp.read().strip()
            assert contents == "FOO=BAR"


def test_set_value_as_base64():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            vantage, ["--env", "test", "__env", "--base64", "FOO=BAR"]
        )
        assert result.exit_code == 0
        assert result.output == ""
        with open("test", "r") as fp:
            contents = fp.read().strip()
            assert contents == "FOO=base64:QkFS"
