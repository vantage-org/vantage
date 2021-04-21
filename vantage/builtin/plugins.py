import argparse
import shutil
from pathlib import Path

from vantage import utils

parser = argparse.ArgumentParser(
    prog="vantage __plugins",
    description="Manage vantage plugins",
    allow_abbrev=False,
)

subparsers = parser.add_subparsers()

parser_install = subparsers.add_parser("install", help="Install a plugin")
parser_install.add_argument(
    "name",
    help="The name of the plugin to install",
)

parser_uninstall = subparsers.add_parser("uninstall", help="Uninstall a plugin")
parser_uninstall.add_argument(
    "name",
    help="The name of the plugin to uninstall",
)

parser_upgrade = subparsers.add_parser("upgrade", help="Upgrade a plugin")
parser_upgrade.add_argument(
    "name",
    help="The name of the plugin to upgrade",
)


def plugins_cmd(env, *args):
    utils.loquacious("Running __plugins", env)
    utils.loquacious(f"  With args: {args}", env)
    args = parser.parse_args(args)
    args.func(env, args.name)


def install(env, name):
    """Install a vantage plugin. NAME can be the name of an official vantage
    plugin, or an absolute URL to any other vantage-compatible gzipped file.

    e.g. vantage __plugins install pg
    """
    url = name
    if url.startswith("https://"):
        _, name = url.rsplit("/", 1)
        name, _ = name.split(".", 1)
    else:
        url = utils.determine_github_latest_release(name)
    utils.download_tarball(url, Path(env["VG_APP_DIR"]) / ".vg-plugins" / name)


def uninstall(env, name):
    shutil.rmtree(Path(env["VG_APP_DIR"]) / ".vg-plugins" / name)


def upgrade(env, name):
    uninstall(env, name)
    install(env, name)


parser_install.set_defaults(func=install)
parser_uninstall.set_defaults(func=uninstall)
parser_upgrade.set_defaults(func=upgrade)
