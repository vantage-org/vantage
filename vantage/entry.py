import argparse
import os
import sys
from pathlib import Path

from vantage import utils, exceptions

from vantage.builtin.env import env_cmd, parser as env_parser
from vantage.builtin.init import init_cmd, parser as init_parser
from vantage.builtin.plugins import plugins_cmd, parser as plugins_parser
from vantage.builtin.tasks import list_tasks_cmd
from vantage.builtin.version import version_cmd
from vantage.shell import shell_cmd
from vantage.task import execute_task_cmd


parser = argparse.ArgumentParser(
    prog="vantage",
    usage="vantage [-a PATH] [-e NAME ...] [-v KEY=[VALUE] ...] [--verbose] [-h] COMMAND...",
    description="Run COMMAND inside a dynamic environment",
    epilog="\n".join(
        [
            "builtin commands:",
            f"  __env      {env_parser.description}",
            f"  __init     {init_parser.description}",
            f"  __plugins  {plugins_parser.description}",
            "  __tasks    Lists all available tasks",
            "  __version  Print current vantage version number",
            "",
            "See the GitHub repo for more details: https://github.com/vantage-org/vantage",
        ]
    ),
    allow_abbrev=False,
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    "-a",
    "--app",
    metavar="PATH",
    help="Set the app directory, the base dir from which every command is run",
)
parser.add_argument(
    "-e",
    "--env",
    metavar="NAME",
    action="append",
    help="Add an env file to the environment",
)
parser.add_argument(
    "-v",
    "--var",
    action="append",
    help="Add a single variable to the environment",
    metavar="KEY[=VALUE]",
)
parser.add_argument(
    "--verbose", action="store_true", help="Print verbose debug messages to stdout"
)
parser.add_argument(
    "-h", "--help", action="store_true", help="Show this help message and exit"
)


def vantage():
    try:
        vg_args, other_args = split_vantage_args(sys.argv[1:])
        vg_args = parser.parse_args(vg_args)

        app = find_app(vg_args.app)
        env = get_env_vars(app, vg_args.env or [], vg_args.var or [])
        env.setdefault("VG_VERBOSE", "1" if vg_args.verbose else "")
        if env["VG_VERBOSE"]:
            utils.loquacious("Compiled ENV is:", env)
            for key, val in env.items():
                utils.loquacious(f"  {key}={val}", env)

        if vg_args.help or len(other_args) == 0:
            parser.print_help()
            list_tasks_cmd(env)
            sys.exit(0)

        builtins = {
            "__env": env_cmd,
            "__init": init_cmd,
            "__plugins": plugins_cmd,
            "__tasks": list_tasks_cmd,
            "__version": version_cmd,
        }
        builtin = builtins.get(other_args[0], None)
        if builtin:
            builtin(env, *other_args[1:])
        else:
            task_path, task_args = get_task_path(env, *other_args)
            if task_path:
                execute_task_cmd(env, task_path, *task_args)
            else:
                shell_cmd(env, *other_args)
    except exceptions.VantageException as ve:
        print(f"vantage: error: {ve.msg}", file=sys.stderr)
        sys.exit(1)


def split_vantage_args(all_args):
    """Returns two lists of arguments; the first are args that should be used by
    vantage itself, the second is a list of everything else."""
    vg_args = []
    append_next = False
    for idx, arg in enumerate(all_args):
        found_unknown = True
        if append_next:
            vg_args.append(arg)
            append_next = False
            found_unknown = False
        if arg in ["-a", "--app", "-e", "--env", "-v", "--var"]:
            vg_args.append(arg)
            append_next = True
            found_unknown = False
        if arg in ["--verbose", "-h", "--help"]:
            vg_args.append(arg)
            found_unknown = False
        if found_unknown:
            return vg_args, all_args[idx:]
    return vg_args, []


def find_app(path=None):
    if path is not None:
        p = Path(path)
        if p.exists():
            return p.resolve()
        raise exceptions.VantageException(f"App directory '{path}' does not exist")
    cwd = p = Path(".").resolve()
    vg_file = p / ".vantage"
    while not vg_file.exists():
        p = p.parent
        if str(p) == p.root:
            return cwd
        vg_file = p / ".vantage"
    return p


def get_env_vars(app, env, var):
    env_vars = utils.load_env_from_file(app / ".vantage", ignore_missing=True)
    env_vars["VG_APP_DIR"] = str(app)
    default_env = None
    env_dir = find_env_dir(app, env_vars)
    if env_dir:
        env_vars["VG_ENV_DIR"] = str(env_dir)
    if "VG_ENV_FILE" in os.environ:
        env_vars["VG_ENV_FILE"] = os.environ["VG_ENV_FILE"]
        parent_env = utils.load_env_from_file(Path(env_vars["VG_ENV_FILE"]))
        parent_env.update(env_vars)
        env_vars = parent_env
    elif "VG_DEFAULT_ENV" in env_vars:
        default_env = Path(env_vars["VG_DEFAULT_ENV"])
        if not default_env.is_file() and env_dir:
            default_env = env_dir / env_vars["VG_DEFAULT_ENV"]
        if not default_env.is_file():
            exceptions.VantageException(
                f"The default env file '{env_vars['VG_DEFAULT_ENV']}' does not exist"
            )
        env_vars.update(utils.load_env_from_file(default_env))
    for env_file in env:
        path = Path(env_file)
        if not path.is_file() and env_dir:
            path = env_dir / path
        if path.is_file():
            env_vars.update(utils.load_env_from_file(path))
        env_vars["VG_ENV_FILE"] = str(path.resolve())
    for key, val in utils.get_env_from_key_val_list(var):
        env_vars[key] = val
    if "VG_ENV_FILE" not in env_vars and default_env:
        env_vars["VG_ENV_FILE"] = str(default_env)
    return env_vars


def find_env_dir(app, env):
    if "VG_ENV_DIR" in env:
        return Path(env["VG_ENV_DIR"])
    p = app / ".env"
    if p.is_dir():
        return p


def get_task_path(env, name, *args):
    plugins_dir = utils.get_plugins_dir(env)
    if plugins_dir.is_dir():
        task, args = get_task_from_dir(env, plugins_dir, name, *args)
        if task:
            return task, args

    task_dir = utils.get_task_dir(env)
    if task_dir.is_dir():
        task, args = get_task_from_dir(env, task_dir, name, *args)
        if task:
            return task, args
    return None, []


def get_task_from_dir(env, dir_, name, *args):
    utils.loquacious(f"Trying to find {name} in {dir_}", env)
    task_path = dir_ / name

    if utils.is_executable(task_path):
        utils.loquacious(f"It's an executable script: {task_path}", env)
        return task_path, args

    for task_path in dir_.glob(f"{name}.*"):
        if utils.is_executable(task_path):
            utils.loquacious(
                f"It's an executable script with a file ext: {task_path}", env
            )
            return task_path, args

    if task_path.is_dir():
        utils.loquacious(f"It's a folder of other tasks: {task_path}", env)

        if args:
            sub_path, sub_args = get_task_from_dir(env, task_path, *args)
            if sub_path:
                utils.loquacious(f"Found sub task: {sub_path}", env)
                return sub_path, sub_args

        nested, nested_args = get_task_from_dir(env, task_path, name, *args)
        if nested:
            utils.loquacious(
                f"It's an executable script inside a folder of the same name: {nested}",
                env,
            )
            return nested, nested_args

    return None, []
