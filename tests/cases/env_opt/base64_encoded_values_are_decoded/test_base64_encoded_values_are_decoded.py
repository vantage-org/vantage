def test_base64_encoded_values_are_decoded(result):
    lines = result.stdout_.splitlines()
    assert "FOO=BAR" in lines
