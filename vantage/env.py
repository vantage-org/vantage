from pathlib import Path

import click

from vantage import utils


@click.command(name="__env")
@click.option(
    "-b",
    "--base64",
    is_flag=True,
    help="When setting a var convert it to base64 first",
)
@click.option(
    "-s",
    "--stdin",
    is_flag=True,
    help="When setting a var read the value from stdin",
)
@click.argument("key_val", required=False)
@click.pass_obj
def env(env, key_val=None, base64=False, stdin=False):
    """Read and set environment variables and files"""
    utils.loquacious("Running __env")
    if key_val is None:
        utils.loquacious("  Printing ENV")
        for k, v in env.items():
            click.echo(f"{k}={v}")
    elif "=" in key_val:
        utils.loquacious("  Setting ENV value")
        key, val = key_val.split("=", 1)
        write_env_value(env, key, val, base64)
    elif stdin:
        utils.loquacious("  Setting ENV value from stdin")
        val = click.get_text_stream("stdin").read().strip()
        write_env_value(env, key_val, val, base64)
    else:
        utils.loquacious("  Printing single ENV value")
        try:
            value = env[key_val]
            click.echo(value)
        except KeyError:
            raise click.ClickException(f"No value found for '{key_val}'")


def write_env_value(env, key, value, base64=False):
    try:
        env_file = Path(env["VG_ENV_FILE"])
        utils.loquacious(f"  Adding {key}={value} to {env_file}")
        if base64:
            value = utils.to_base64(value)
        env[key] = value
        with env_file.open("w") as fp:
            for key, value in sorted(env.items()):
                if not key.startswith("VG_"):
                    fp.write(f"{key}={value}\n")
    except KeyError:
        raise click.ClickException(
            "No env file provided, there's nowhere to store this value"
        )
