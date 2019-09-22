from click.testing import CliRunner
from vantage.entry import vantage


def test_can_add_single_var():
    runner = CliRunner()
    result = runner.invoke(vantage, ["--var", "FOO=BAR", "env"])
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert "FOO=BAR" in lines


def test_can_add_multiple_vars():
    runner = CliRunner()
    result = runner.invoke(vantage, ["--var", "FOO=BAR", "--var", "FOO2=BAR2", "env"])
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert "FOO=BAR" in lines
    assert "FOO2=BAR2" in lines


def test_if_no_value_given_then_prompted():
    runner = CliRunner()
    result = runner.invoke(vantage, ["--var", "FOO", "env"], input="BAR\n")
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert "FOO=BAR" in lines


def test_base64_encoded_values_are_decoded():
    runner = CliRunner()
    result = runner.invoke(vantage, ["--var", "FOO=base64:QkFS", "env"])
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert "FOO=BAR" in lines
