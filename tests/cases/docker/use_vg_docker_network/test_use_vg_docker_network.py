def test_use_vg_docker_network(stdout, stderr):
    # The task should print the network ID, if it doesn't have an ID then
    # "" is printed instead.
    assert '""' not in stdout
