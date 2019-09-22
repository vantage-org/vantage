import sys
import os
from pathlib import Path

import click

from vantage import utils
from vantage.env import env as env_cmd
from vantage.shell import shell as shell_cmd

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class VantageCLI(click.MultiCommand):

    def list_commands(self, ctx):
        return ["__env", "__plugins", "__update"]

    def get_command(self, ctx, name):
        if name == "__env":
            return env_cmd
        params = [click.Argument(("args",), nargs=-1, required=False)]
        return click.Command(name, params=params, callback=shell_cmd)


@click.command(
    cls=VantageCLI, context_settings=CONTEXT_SETTINGS, invoke_without_command=True
)
@click.option("-a", "--app", help="Set the app directory")
@click.option("-e", "--env", multiple=True, help="Add an env file to the environment")
@click.option(
    "-v", "--var", multiple=True, help="Add a single variable to the environment"
)
@click.pass_context
def vantage(ctx, app=None, env=tuple(), var=tuple()):
    """Run CMD with environment variables

    \b
    CMD can be:
        __env - Read and write your app's environment values
        __plugins - Manage vantage plugins
        __update - Update vantage and it's plugins
        TASK - The name of a task in your tasks directory
        * - Any other command at all

    See the GitHub repo for more details (https://github.com/vantage-org/vantage)"""
    app = find_app(app)
    env_vars = get_env_vars(app, env, var)
    ctx.obj = env_vars


def find_app(path=None):
    if path is not None:
        p = Path(path)
        if p.exists():
            return p.resolve()
        raise click.ClickException(f"App directory '{p}' does not exist")
    cwd = p = Path(".").resolve()
    vg_file = p / ".vantage"
    while not vg_file.exists():
        p = p.parent
        if str(p) == p.root:
            return cwd
        vg_file = p / ".vantage"
    return p


def get_env_vars(app, env, var):
    env_vars = load_env_from_file(app / ".vantage", ignore_missing=True)
    env_vars["VG_APP_DIR"] = str(app)
    env_dir = find_env_dir(app)
    if env_dir:
        env_vars["VG_ENV_DIR"] = str(env_dir)
    if "VG_ENV_FILE" in os.environ:
        env_vars["VG_ENV_FILE"] = os.environ["VG_ENV_FILE"]
        parent_env = load_env_from_file(env_vars["VG_PARENT_ENV_FILE"])
        parent_env.update(env_vars)
        env_vars = parent_env
    elif "VG_DEFAULT_ENV" in env_vars:
        env_vars.update(load_env_from_file(env_vars["VG_DEFAULT_ENV"]))
    for env_file in env:
        path = Path(env_file)
        if not path.is_file() and env_dir:
            path = env_dir / path
        if path.is_file():
            env_vars.update(load_env_from_file(path))
        if "VG_ENV_FILE" not in env_vars:
            env_vars["VG_ENV_FILE"] = str(path.resolve())
    for key, val in get_env_vars_from_var_options(var):
        env_vars[key] = val
    return env_vars


def get_env_vars_from_var_options(var):
    for key_val in var:
        if "=" in key_val:
            key, val = key_val.split("=", 1)
        else:
            key = key_val
            if utils.has_stdin():
                val = click.get_text_stream("stdin").read().strip()
            else:
                val = click.prompt(f"Input required {key}=", prompt_suffix="")
        val = utils.from_base64(val.strip())
        yield key, val


def find_env_dir(app):
    p = app / ".env"
    if p.is_dir():
        return p


def load_env_from_file(path, ignore_missing=False):
    env = {}
    try:
        with path.open() as fp:
            for line in fp:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    value = utils.from_base64(value.strip())
                    env[key.strip()] = value
    except FileNotFoundError:
        if not ignore_missing:
            raise click.ClickException(f"The env file '{path}' does not exist")
    return env
