def test_see_for_top_level(result):
    assert (
        "usage: vantage [-a PATH] [-e NAME ...] [-v KEY=[VALUE] ...] [--verbose] [-h] COMMAND..."
        in result.stdout_
    )
