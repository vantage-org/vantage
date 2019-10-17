import os
import sys
from pathlib import Path

import click

from vantage import utils, task
from vantage.env import env as env_cmd
from vantage.init import init as init_cmd
from vantage.plugins import plugins as plugins_cmd
from vantage.shell import shell as shell_cmd

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class VantageCLI(click.MultiCommand):

    def list_commands(self, ctx):
        # Invoke here to get the ctx populated
        click.Command.invoke(self, ctx)
        tasks = task.get_task_names(ctx.obj)
        return list(tasks) + ["__env", "__init", "__plugins"]

    def get_command(self, ctx, name):
        # Invoke here to get the ctx populated
        click.Command.invoke(self, ctx)
        # First try vantage builtins
        if name == "__env":
            return env_cmd
        if name == "__init":
            return init_cmd
        if name == "__plugins":
            return plugins_cmd
        # Then a project task file or an installed plugin task file
        task_ = task.get_task(ctx.obj, name)
        if task_:
            return task_
        # Fallback to shelling out
        params = [click.Argument(("args",), nargs=-1, required=False)]
        return click.Command(name, params=params, callback=shell_cmd)


@click.command(
    cls=VantageCLI, context_settings=CONTEXT_SETTINGS, invoke_without_command=True
)
@click.option(
    "-a",
    "--app",
    help="Set the app directory, the base dir from which every command is run",
)
@click.option("-e", "--env", multiple=True, help="Add an env file to the environment")
@click.option(
    "-v", "--var", multiple=True, help="Add a single variable to the environment"
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Print verbose debug messages to stdout",
)
@click.pass_context
def vantage(ctx, app=None, env=None, var=None, verbose=False):
    """Run COMMAND inside a dynamic environment

    \b
    See the GitHub repo for more details:
    https://github.com/vantage-org/vantage"""
    if ctx.obj is None:
        env = env or tuple()
        var = var or tuple()
        app = find_app(app)
        env_vars = get_env_vars(app, env, var)
        env_vars.setdefault("VG_VERBOSE", "1" if verbose else "")
        if env_vars["VG_VERBOSE"]:
            utils.loquacious("Compiled ENV is:")
            for key, val in env_vars.items():
                utils.loquacious(f"  {key}={val}")
        ctx.obj = env_vars
    click.echo(ctx.obj["VG_BINARY"])


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
    env_dir = find_env_dir(app, env_vars)
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
    env_vars["VG_BINARY"] = get_binary()
    return env_vars


def get_binary():
    if getattr(sys, "frozen", False):
        return sys.executable
    return os.path.abspath(__file__)


def get_env_vars_from_var_options(var):
    for key_val in var:
        if "=" in key_val:
            key, val = key_val.split("=", 1)
        else:
            key = key_val
            val = click.prompt(f"Input required {key}=", prompt_suffix="")
        val = utils.from_base64(val.strip())
        yield key, val


def find_env_dir(app, env):
    if "VG_ENV_DIR" in env:
        return env["VG_ENV_DIR"]
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
