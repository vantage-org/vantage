def test_load_from_single_file(result):
    lines = result.stdout_.splitlines()
    assert "FOO=BAR" in lines
