def test_run_required_first(result):
    lines = result.stdout_.splitlines()
    assert lines == ["first!", "something!"]
