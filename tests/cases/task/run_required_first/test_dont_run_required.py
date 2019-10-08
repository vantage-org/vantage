def test_dont_run_required(result):
    lines = result.stdout_.splitlines()
    assert lines == ["something!"]
