def test_set_to_cwd(result):
    assert result.exit_code == 0
    for line in result.stdout_.splitlines():
        if line.startswith("VG_APP_DIR="):
            assert "set_to_cwd" in line
            assert line.endswith("/case")
