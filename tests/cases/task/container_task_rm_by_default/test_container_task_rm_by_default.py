import sh


def test_container_task_rm_by_default(run):
    count_before = len(sh.docker("ps", all=True).stdout.splitlines())
    run()
    count_after = len(sh.docker("ps", all=True).stdout.splitlines())
    assert count_before == count_after
