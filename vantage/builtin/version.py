from vantage import utils


def version_cmd(env, *args):
    utils.loquacious("Running __version command", env)
    latest = utils.determine_github_latest_release("vantage")
    latest = latest["name"].split("-")[1]
    print("Installed version: 3.4.0")
    print(f"   Latest version: {latest}")
