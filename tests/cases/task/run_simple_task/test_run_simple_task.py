def test_run_simple_task(result):
    lines = result.stdout_.splitlines()
    assert lines == ["something!"]
