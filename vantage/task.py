import sys
import os
from functools import partial, lru_cache
from pathlib import Path

import click
import sh
import yaml

from vantage import utils


@click.pass_context
def task_cmd(ctx, path, args, run_required=None):
    env = ctx.obj
    utils.loquacious(f"Running task in {path}")
    meta = load_meta(path)
    env = update_env(meta, env)
    run_required = get_flag(
        opt=run_required,
        env=env.get("VG_RUN_REQUIRED"),
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
            utils.loquacious(f"  Spinning up docker image")
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
                tag = image.pop("tag")
                for k, v in image.items():
                    if isinstance(v, list):
                        for w in v:
                            run_args += [f"--{k}", insert_env_vals(w, env)]
                    elif isinstance(v, bool):
                        if v:
                            run_args += [f"--{k}"]
                    else:
                        run_args += [f"--{k}", insert_env_vals(v, env)]
            else:
                tag = image
                run_args += ["--rm"]
            for e in env.keys():
                run_args += ["--env", e]
            run_args += [tag, "/vg-task"]
            args = run_args + list(args)
        else:
            utils.loquacious(f"  Passing task over to sh")
            cmd = sh.Command(str(path))
        cmd(
            *args,
            _out=click.get_text_stream("stdout"),
            _err=click.get_text_stream("stderr"),
            _in=click.get_text_stream("stdin"),
            _tty_in=tty_in,
            _env=env,
            _cwd=env["VG_APP_DIR"],
        )
    except sh.ErrorReturnCode as erc:
        utils.loquacious(f"  Something went wrong, returned exit code {erc.exit_code}")
        return sys.exit(erc.exit_code)


def insert_env_vals(str, env):
    for k, v in env.items():
        needle = f"${k}"
        if needle in str:
            str = str.replace(needle, v)
    return str


@lru_cache()
def load_meta(path):
    utils.loquacious(f"  Loading meta from task file")
    with path.open() as f:
        content = f.read()
        sep = None
        for line in content.splitlines():
            if "---" in line:
                sep = line
                break
        if sep is None:
            utils.loquacious(f"  No meta found")
            return {}
        else:
            _, meta, script = content.split(sep, 2)
            comment_marker = sep.replace("---", "")
            utils.loquacious(f"  Meta commented out using '{comment_marker}'")
            meta = meta.replace(f"\n{comment_marker}", "\n")
            return yaml.load(meta, Loader=yaml.SafeLoader)


def update_env(meta, env):
    env_vars = meta.get("variables")
    if env_vars is not None:
        if env["VG_VERBOSE"]:
            utils.loquacious("  Updating env with vars in task meta")
            for key, val in env_vars.items():
                utils.loquacious(f"    {key}={val}")
        env.update(env_vars)
    return env


def get_flag(opt, env, yml, default):
    if opt is None:
        if env is None:
            if yml is None:
                return default
            return yml
        return env
    return opt


def is_executable(path):
    return path.is_file() and os.access(path, os.X_OK)


def get_task(env, name):
    task_dir = get_task_dir(env)
    plugins_dir = get_plugins_dir(env)

    for dir_ in (task_dir, plugins_dir):
        if dir_.is_dir():
            return get_task_from_dir(dir_, name)


def get_task_from_dir(dir_, name):
    task_path = dir_ / name
    if is_executable(task_path):
        return as_command(task_path)

    if task_path.is_dir():
        nested = get_task_from_dir(task_path, name)
        if nested:
            return nested
        return as_group(task_path)

    for task_path in dir_.glob(f"{name}.*"):
        if is_executable(task_path):
            return as_command(task_path)


@lru_cache()
def as_command(path):
    meta = load_meta(path)
    params = [
        click.Option(("--run-required/--skip-required",)),
        click.Argument(("args",), nargs=-1, type=click.UNPROCESSED),
    ]
    return click.Command(
        path.stem,
        callback=partial(task_cmd, path=path),
        context_settings=dict(allow_extra_args=True, ignore_unknown_options=True),
        params=params,
        short_help=meta.get("help-text"),
        help=meta.get("help-text"),
    )


@lru_cache()
def as_group(path, walk=True):
    group = click.Group(name=path.stem)
    if walk:
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
