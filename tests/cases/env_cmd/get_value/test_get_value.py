def test_get_value(result):
    assert result.exit_code == 0
    assert result.stdout_ == "BAR"
