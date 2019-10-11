def test_run_task_inside_container(result):
    assert "linuxkit" in result.stdout_
