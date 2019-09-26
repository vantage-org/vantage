def test_list_all(result):
    assert result.exit_code == 0
    env = dict(line.split("=", 1) for line in result.stdout_.splitlines())
    assert "VG_APP_DIR" in env
    assert env["FOO"] == "BAR"
