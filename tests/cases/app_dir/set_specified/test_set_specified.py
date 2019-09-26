def test_set_specified(result):
    assert result.exit_code == 0
    assert "VG_APP_DIR=/usr/local" in result.stdout_.splitlines()
