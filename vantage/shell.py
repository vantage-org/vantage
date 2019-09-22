import sys

import click
import sh


@click.pass_context
def shell(ctx, args):
    try:
        command = sh.Command(ctx.command.name)
        command(
            *args,
            _env=ctx.obj,
            _out=click.get_text_stream("stdout"),
            _err=click.get_text_stream("stderr"),
        )
    except sh.ErrorReturnCode as erc:
        sys.exit(erc.exit_code)
    except sh.CommandNotFound:
        raise click.ClickException(f"Command '{ctx.command.name}' not found")
