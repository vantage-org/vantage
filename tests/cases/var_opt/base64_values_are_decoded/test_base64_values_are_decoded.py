def test_base64_values_are_decoded(result):
    assert "FOO=BAR" in result.stdout_
