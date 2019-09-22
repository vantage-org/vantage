from click.testing import CliRunner
from vantage.entry import vantage


def test_prints_top_level_help():
    runner = CliRunner()
    result = runner.invoke(vantage, ["--help"])
    assert result.exit_code == 0
    assert "Usage: vantage [OPTIONS] COMMAND [ARGS]..." in result.output
    assert "-a, --app TEXT  Set the app directory" in result.output
    assert "-e, --env TEXT  Add an env file to the environment" in result.output
    assert "-v, --var TEXT  Add a single variable to the environment" in result.output
