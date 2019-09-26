def test_set_to_first_parent_with_vg_file(result):
    assert result.exit_code == 0
    for line in result.stdout_.splitlines():
        if line.startswith("VG_APP_DIR="):
            assert "test_set_to_first_parent_with" in line
            assert line.endswith("/parent")
