def test_container_task_inherits_env(result):
    lines = result.stdout_.splitlines()
    assert "FOO=BAR" in lines
