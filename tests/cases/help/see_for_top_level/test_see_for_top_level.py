def test_see_for_top_level(result):
    assert "Usage: vantage [OPTIONS] COMMAND [ARGS]..." in result.stdout_
