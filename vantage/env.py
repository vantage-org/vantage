from pathlib import Path

import click

from . import utils


@click.command(name="__env")
@click.option("-b", "--base64", is_flag=True)
@click.argument("key_val", required=False)
@click.pass_context
def env(ctx, key_val=None, base64=False):
    if key_val is None:
        for k, v in ctx.obj.items():
            click.echo(f"{k}={v}")
    elif "=" in key_val:
        key, val = key_val.split("=", 1)
        write_env_value(ctx, key, val, base64)
    elif utils.has_stdin():
        val = click.get_text_stream("stdin").read().strip()
        write_env_value(ctx, key_val, val, base64)
    else:
        try:
            value = ctx.obj[key_val]
            click.echo(value)
        except KeyError:
            raise click.ClickException(f"No value found for '{key_val}'")


def write_env_value(ctx, key, value, base64=False):
    try:
        env_file = Path(ctx.obj["VG_ENV_FILE"])
        with env_file.open("a") as fp:
            if base64:
                value = utils.to_base64(value)
            fp.write(f"{key}={value}\n")
    except KeyError:
        raise click.ClickException(
            f"No env file provided, I don't know where to store this value"
        )
