def test_set_value_as_base64(result, get_file):
    assert result.exit_code == 0
    env = get_file("test")
    assert env == "FOO=base64:QkFS"
