def test_set_value(result, get_file):
    assert result.exit_code == 0
    env = get_file("test")
    assert env == "FOO=BAR"
