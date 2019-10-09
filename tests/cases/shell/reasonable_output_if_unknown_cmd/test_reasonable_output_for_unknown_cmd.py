def test_reasonable_output_for_unknown_cmd(result):
    assert result.exit_code == 1
    assert result.stderr_ == "Error: Command 'not-a-command' not found"
