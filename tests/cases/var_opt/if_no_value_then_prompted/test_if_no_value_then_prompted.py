def test_if_no_value_then_prompted(result):
    assert "FOO=BAR" in result.stdout_
