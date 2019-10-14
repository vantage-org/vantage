import json
import shutil
import tarfile
import urllib.request
from pathlib import Path

import click


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
        latest_release = urllib.request.urlopen(
            f"https://api.github.com/repos/vantage-org/{name}/releases/latest"
        )
        latest_release = json.load(latest_release)
        for asset in latest_release["assets"]:
            if name in asset["name"]:
                url = asset["browser_download_url"]
                break
    archive, _ = urllib.request.urlretrieve(url, filename=None)
    tar = tarfile.open(archive, mode="r:*")
    tar.extractall(path=Path(env["VG_APP_DIR"]) / ".vg-plugins" / name)


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
