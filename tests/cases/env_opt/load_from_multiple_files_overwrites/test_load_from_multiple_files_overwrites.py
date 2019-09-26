def test_load_from_multiple_files_overwrites(result):
    lines = result.stdout_.splitlines()
    assert "FOO=BAR2" in lines
    assert "FOO=BAR" not in lines
