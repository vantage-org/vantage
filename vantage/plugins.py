import shutil
from pathlib import Path

import click

from vantage import utils


@click.group(name="__plugins")
@click.pass_obj
def plugins(env):
    """Manage vantage plugins"""
    pass


@plugins.command(name="install")
@click.argument("name")
@click.pass_obj
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


@plugins.command(name="uninstall")
@click.argument("name")
@click.pass_obj
def uninstall(env, name):
    shutil.rmtree(Path(env["VG_APP_DIR"]) / ".vg-plugins" / name)


@plugins.command(name="update")
@click.argument("name")
@click.pass_obj
def update(env, name):
    click.invoke(uninstall, name)
    click.invoke(install, name)
