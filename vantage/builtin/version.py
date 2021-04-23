from vantage import utils


def version_cmd(env, *args):
    utils.loquacious("Running __version command", env)
    print("3.1.2")
