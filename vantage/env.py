from pathlib import Path

import click

from vantage import utils


@click.command(name="__env")
@click.option("-b", "--base64", is_flag=True)
@click.option("-s", "--stdin", is_flag=True)
@click.argument("key_val", required=False)
@click.pass_obj
def env(env, key_val=None, base64=False, stdin=False):
    utils.loquacious("Running __env", env=env)
    if key_val is None:
        utils.loquacious("  Printing ENV", env=env)
        for k, v in env.items():
            click.echo(f"{k}={v}")
    elif "=" in key_val:
        utils.loquacious("  Setting ENV value", env=env)
        key, val = key_val.split("=", 1)
        write_env_value(env, key, val, base64)
    elif stdin:
        utils.loquacious("  Setting ENV value from stdin", env=env)
        val = click.get_text_stream("stdin").read().strip()
        write_env_value(env, key_val, val, base64)
    else:
        utils.loquacious("  Printing single ENV value", env=env)
        try:
            value = env[key_val]
            click.echo(value)
        except KeyError:
            raise click.ClickException(f"No value found for '{key_val}'")


def write_env_value(env, key, value, base64=False):
    try:
        env_file = Path(env["VG_ENV_FILE"])
        utils.loquacious(f"  Adding {key}={value} to {env_file}", env=env)
        with env_file.open("a") as fp:
            if base64:
                value = utils.to_base64(value)
            fp.write(f"{key}={value}\n")
    except KeyError:
        raise click.ClickException(
            f"No env file provided, there's nowhere to store this value"
        )
