def test_load_from_named(result):
    lines = result.stdout_.splitlines()
    assert "FOO=BAR" in lines
