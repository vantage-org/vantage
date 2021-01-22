import sys
import os
from functools import partial, lru_cache
from pathlib import Path

import click
import sh
import yaml

from vantage import utils


@click.pass_context
def task_cmd(ctx, path, args):
    env = ctx.obj
    utils.loquacious(f"Running task in {path}")
    meta = load_meta(path)
    env = update_env(meta, env)
    run_required = get_flag(
        env=bool(env.get("VG_RUN_REQUIRED")),
        yml=meta.get("run-required"),
        default=False,
    )
    utils.loquacious(f"  Run required? {'YES' if run_required else 'NO'}")
    if run_required:
        for required in meta.get("requires", []):
            utils.loquacious(f"  Running required task: {required}")
            t = get_task(env, required)
            resp = t.invoke(ctx)
            utils.loquacious(f"  Got resp: {resp}")
    try:
        tty_in = False
        if meta.get("image"):
            utils.loquacious("  Spinning up docker image")
            utils.loquacious(f"  Path is: {os.environ.get('PATH')}")
            cmd = sh.Command("docker")
            image = meta.get("image")
            run_args = [
                "run",
                "--volume",
                f"{str(path)}:/vg-task",
                "--label",
                "vantage",
                "--label",
                "vantage-task",
            ]
            if isinstance(image, dict):
                tty_in = bool(image.get("tty", False))
                tag = insert_env_vals(image.pop("tag"), env, args)
                for k, v in image.items():
                    if isinstance(v, list):
                        for w in v:
                            run_args += [
                                f"--{k}",
                                insert_env_vals(w, env, args),
                            ]
                    elif isinstance(v, bool):
                        if v:
                            run_args += [f"--{k}"]
                    else:
                        run_args += [f"--{k}", insert_env_vals(v, env, args)]
                if "VG_DOCKER_NETWORK" in env and "network" not in image:
                    network = env["VG_DOCKER_NETWORK"]
                    ensure_network(network)
                    run_args += ["--network", network]
            else:
                tag = image
                run_args += ["--rm"]
            for e in env.keys():
                run_args += ["--env", e]
            run_args += [tag, "/vg-task"]
            args = run_args + list(args)
        else:
            utils.loquacious("  Passing task over to sh")
            env["PATH"] = os.environ.get("PATH", "")
            cmd = sh.Command(str(path))
        utils.loquacious(f"Running command {cmd} with args {args}")
        cmd(
            *args,
            _in=sys.stdin,
            _out=sys.stdout,
            _err=sys.stderr,
            _env=env,
            _cwd=env["VG_APP_DIR"],
        )
    except sh.ErrorReturnCode as erc:
        utils.loquacious(
            f"  Something went wrong, returned exit code {erc.exit_code}"
        )
        return sys.exit(erc.exit_code)


def insert_env_vals(haystack, env=None, args=None):
    if env:
        for k, v in env.items():
            needle = f"${k}"
            if needle in haystack:
                haystack = haystack.replace(needle, str(v))
    if args:
        for i, v in enumerate(args):
            needle = f"${i}"
            if needle in haystack:
                haystack = haystack.replace(needle, str(v))
    return haystack


@lru_cache()
def load_meta(path):
    utils.loquacious("  Loading meta from task file")
    with path.open() as f:
        content = f.read()
        sep = None
        for line in content.splitlines():
            if "---" in line:
                sep = line
                break
        if sep is None:
            utils.loquacious("  No meta found")
            return {}
        else:
            _, meta, script = content.split(sep, 2)
            comment_marker = sep.replace("---", "")
            utils.loquacious(f"  Meta commented out using '{comment_marker}'")
            meta = meta.replace(f"\n{comment_marker}", "\n")
            return yaml.load(meta, Loader=yaml.SafeLoader)


def update_env(meta, env):
    if meta.get("env"):
        env_file = meta["env"]
        utils.loquacious("  Using env {env_file} instead")
        return load_env(env_file, current=env)
    overrides = meta.get("overrides")
    if overrides is not None:
        utils.loquacious("  Updating env with override vars in task meta")
        for key, val in overrides.items():
            val = insert_env_vals(val, env)
            env[key] = val
            utils.loquacious(f"    {key}={val}")
    defaults = meta.get("defaults")
    if defaults is not None:
        utils.loquacious("  Updating env with default vars in task meta")
        for key, val in defaults.items():
            if key not in env:
                val = insert_env_vals(val, env)
                env[key] = val
                utils.loquacious(f"    {key}={val}")
    return env


def load_env(name_or_path, current):
    new_env = None
    path = Path(name_or_path)
    if path.is_file():
        new_env = utils.load_env_from_file(path)
    else:
        env_dir = current.get("VG_ENV_DIR")
        if env_dir:
            path = Path(env_dir) / name_or_path
            if path.is_file():
                new_env = utils.load_env_from_file(path)
    if new_env is None:
        raise click.ClickException(
            f"The env file '{name_or_path}' does not exist"
        )
    for k, v in current.items():
        if k.startswith("VG_") and k not in new_env:
            new_env[k] = v
    return new_env


def get_flag(env, yml, default):
    if env is None:
        if yml is None:
            return default
        return yml
    return env


def is_executable(path):
    return path.is_file() and os.access(path, os.X_OK)


def ensure_network(name):
    sh.docker("network", "create", name, _ok_code=[0, 1])


def get_task(env, name):
    task_dir = get_task_dir(env)
    plugins_dir = get_plugins_dir(env)

    for dir_ in (task_dir, plugins_dir):
        utils.loquacious(f"Looking in {dir_} for task file")
        if dir_.is_dir():
            task = get_task_from_dir(dir_, name)
            if task is not None:
                return task


def get_task_from_dir(dir_, name):
    utils.loquacious(f"Trying to find {name} in {dir_}")
    task_path = dir_ / name
    if is_executable(task_path):
        utils.loquacious("It's an executable script")
        return as_command(task_path)

    for task_path in dir_.glob(f"{name}.*"):
        if is_executable(task_path):
            utils.loquacious("It's an executable script with a file ext")
            return as_command(task_path)

    if task_path.is_dir():
        nested = get_task_from_dir(task_path, name)
        if nested:
            utils.loquacious(
                "It's an executable script inside a folder of the same name"
            )
            return nested
        utils.loquacious("It's a folder of other tasks")
        return as_group(task_path)


@lru_cache()
def as_command(path):
    utils.loquacious(f"Building {path} as a command")
    meta = load_meta(path)
    params = [click.Argument(("args",), nargs=-1, type=click.UNPROCESSED)]
    return click.Command(
        path.stem,
        callback=partial(task_cmd, path=path),
        context_settings=dict(
            allow_extra_args=True, ignore_unknown_options=True
        ),
        params=params,
        short_help=meta.get("help-text"),
        help=meta.get("help-text"),
    )


@lru_cache()
def as_group(path, walk=True):
    utils.loquacious(f"Building {path} as a group")
    group = click.Group(name=path.stem)
    if walk:
        utils.loquacious("Walking the file tree looking for sub commands")
        for task_path in path.iterdir():
            if task_path.is_dir():
                group.add_command(as_group(task_path, walk=False))
            elif is_executable(task_path):
                group.add_command(as_command(task_path))
    return group


def get_task_names(env):
    task_dir = get_task_dir(env)
    plugins_dir = get_plugins_dir(env)

    for dir_ in (task_dir, plugins_dir):
        if dir_.is_dir():
            utils.loquacious(f"Listing tasks inside {dir_}")
            for task_path in dir_.iterdir():
                if task_path.is_dir() or is_executable(task_path):
                    yield task_path.stem


def get_task_dir(env):
    if env.get("VG_TASKS_DIR"):
        return Path(env.get("VG_TASKS_DIR"))
    return Path(env["VG_APP_DIR"]) / "tasks"


def get_plugins_dir(env):
    if env.get("VG_PLUGINS_DIR"):
        return Path(env.get("VG_PLUGINS_DIR"))
    return Path(env["VG_APP_DIR"]) / ".vg-plugins"
