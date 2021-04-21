def test_errors_if_no_env_file_to_save_to(result):
    assert result.exit_code == 1
    err = "vantage: error: No env file provided, there's nowhere to store this value"
    assert result.stderr_ == err
