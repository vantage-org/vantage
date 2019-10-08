def test_pass_remaining_cli_args_to_task(result):
    lines = result.stdout_.splitlines()
    assert lines == ["--arg something!"]
