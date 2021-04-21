def test_errors_if_dir_doesnt_exist(result):
    assert result.exit_code == 1
    assert result.stderr_ == "vantage: error: App directory '/not-a-dir' does not exist"
