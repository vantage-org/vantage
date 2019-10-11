def test_override_default_container_options(stdout):
    lines = stdout.splitlines()
    is_found = ["test_override_default_container_options.py" in l for l in lines]
    assert any(is_found)
