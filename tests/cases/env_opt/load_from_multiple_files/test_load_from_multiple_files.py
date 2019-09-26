def test_load_from_multiple_files(result):
    lines = result.stdout_.splitlines()
    assert "FOO=BAR" in lines
    assert "FOO2=BAR2" in lines
