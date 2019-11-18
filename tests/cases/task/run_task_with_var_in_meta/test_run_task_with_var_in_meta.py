def test_run_task_with_var_in_meta(result):
    lines = result.stdout_.splitlines()
    assert lines == ["one, two, three"]
