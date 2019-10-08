import sys

import click
import sh
from vantage import utils


@click.pass_context
def shell(ctx, args):
    utils.loquacious(f"Running '{ctx.command.name}' in shell", env=ctx.obj)
    utils.loquacious(f"  With args: {args}", env=ctx.obj)
    try:
        command = sh.Command(ctx.command.name)
        command(
            *args,
            _env=ctx.obj,
            _out=click.get_text_stream("stdout"),
            _err=click.get_text_stream("stderr"),
        )
    except sh.ErrorReturnCode as erc:
        utils.loquacious(f"  Exited with code {erc.exit_code}", env=ctx.obj)
        sys.exit(erc.exit_code)
    except sh.CommandNotFound:
        raise click.ClickException(f"Command '{ctx.command.name}' not found")
