def test_run_other_nested_task(result):
    lines = result.stdout_.splitlines()
    assert lines == ["something!"]
