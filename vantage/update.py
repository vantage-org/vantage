"""
__update
"""
import click


@click.command(name="__update")
@click.pass_obj
def update(env, args):
    """Self update this vantage istallation"""
    raise click.ClickException("Not implemented")
