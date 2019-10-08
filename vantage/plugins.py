"""
__plugins
__plugins install NAME_OR_URL
__plugins update NAME
__plugins uninstall NAME
"""
import click


@click.command(name="__plugins")
@click.pass_obj
def plugins(env, args):
    raise click.ClickException("Not implemented")
