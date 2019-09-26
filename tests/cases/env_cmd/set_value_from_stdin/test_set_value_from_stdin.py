def test_set_value_from_stdin(result, get_file):
    assert result.exit_code == 0
    env_file = get_file("test")
    assert env_file == "FOO=BAR"
