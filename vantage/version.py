import click
from vantage import utils


@click.command(name="__version")
def version():
    utils.loquacious("Running __version command")
    click.echo("3.0.3")
