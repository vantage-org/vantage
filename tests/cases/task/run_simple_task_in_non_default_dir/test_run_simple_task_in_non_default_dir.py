def test_run_simple_task_in_non_default_dir(result):
    lines = result.stdout_.splitlines()
    assert lines == ["something!"]
