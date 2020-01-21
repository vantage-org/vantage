import shutil
from pathlib import Path

import click

from vantage import utils


@click.command(name="__update")
@click.pass_context
def update(ctx):
    utils.loquacious("Self-updating this vantage installation")
    install_dir = Path("/usr/local/vantage")
    if not install_dir.is_dir():
        raise click.ClickException(
            "__update only works if vantage has been installed to the default directory (/usr/local/vantage)"
        )
    utils.loquacious("  Confirmed install dir")
    url = utils.determine_github_latest_release("vantage")
    utils.download_tarball(url, "/usr/local/vantage-tmp")
    utils.loquacious("  Downloaded latest vantage release")
    shutil.rmtree("/usr/local/vantage")
    shutil.move("/usr/local/vantage-tmp/vantage", "/usr/local/vantage")
    shutil.rmtree("/usr/local/vantage-tmp")
    utils.loquacious("  Installed!")
