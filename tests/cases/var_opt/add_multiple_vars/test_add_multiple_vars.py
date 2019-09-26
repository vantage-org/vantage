def test_add_multiple_vars(result):
    lines = result.stdout_.splitlines()
    assert "FOO=BAR" in lines
    assert "FOO2=BAR2" in lines
