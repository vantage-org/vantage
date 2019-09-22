from click.testing import CliRunner
from vantage.entry import vantage


def test_single_env_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("env_file", "w") as fp:
            fp.write("FOO=BAR\n")
        result = runner.invoke(vantage, ["--env", "env_file", "env"])
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert "FOO=BAR" in lines


def test_multiple_env_files():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("env_file", "w") as fp:
            fp.write("FOO=BAR\n")
        with open("env_file2", "w") as fp:
            fp.write("FOO2=BAR2\n")
        result = runner.invoke(
            vantage, ["--env", "env_file", "--env", "env_file2", "env"]
        )
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert "FOO=BAR" in lines
    assert "FOO2=BAR2" in lines


def test_subsequent_env_files_overwrite():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("env_file", "w") as fp:
            fp.write("FOO=BAR\n")
        with open("env_file2", "w") as fp:
            fp.write("FOO=BAR2\n")
        result = runner.invoke(
            vantage, ["--env", "env_file", "--env", "env_file2", "env"]
        )
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert "FOO=BAR" not in lines
    assert "FOO=BAR2" in lines


def test_base64_encoded_values_are_decoded():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("env_file", "w") as fp:
            fp.write("FOO=base64:QkFS\n")
        result = runner.invoke(vantage, ["--env", "env_file", "env"])
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert "FOO=BAR" in lines
