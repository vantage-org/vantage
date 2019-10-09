import sys
import os
from functools import partial, lru_cache
from pathlib import Path

import click
import sh
import yaml

from vantage import utils


@click.pass_context
def task_cmd(ctx, path, args, run_required=None, keep_image=None):
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
    keep_image = get_flag(
        opt=keep_image,
        env=env.get("VG_KEEP_IMAGE"),
        yml=meta.get("keep-image"),
        default=False,
    )
    utils.loquacious(f"  Run required? {'YES' if run_required else 'NO'}")
    utils.loquacious(f"  Keep image? {'YES' if keep_image else 'NO'}")
    if run_required:
        for required in meta.get("requires", []):
            utils.loquacious(f"  Running required task: {required}")
            t = get_task(env, required)
            resp = t.invoke(ctx)
            utils.loquacious(f"  Got resp: {resp}")
    if meta.get("image"):
        # Run image
        # sh.docker("run", etc. etc.)
        pass
    utils.loquacious(f"  Passing task over to sh")
    try:
        cmd = sh.Command(str(path))
        cmd(
            *args,
            _out=click.get_text_stream("stdout"),
            _err=click.get_text_stream("stderr"),
            _in=click.get_text_stream("stdin"),
            _env=env,
            _cwd=env["VG_APP_DIR"],
        )
    except sh.ErrorReturnCode as erc:
        utils.loquacious(f"  Something went wrong, returned exit code {erc.exit_code}")
        return sys.exit(erc.exit_code)
    finally:
        if meta.get("image") and not keep_image:
            # Rm image
            # sh.docker("stop", etc. etc.)
            pass


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


def get_task(env, name):
    task_dir = get_task_dir(env)
    plugins_dir = get_plugins_dir(env)

    for dir_ in (task_dir, plugins_dir):
        if dir_.is_dir():
            for stem in (name, f"{name}/{name}"):
                for task_path in dir_.glob(f"{stem}*"):
                    if os.access(task_path, os.X_OK):
                        return as_command(task_path)


@lru_cache()
def as_command(path):
    meta = load_meta(path)
    params = [
        click.Option(("--run-required/--skip-required",)),
        click.Option(("--keep-image/--rm-image",)),
        click.Argument(("args",), nargs=-1, type=click.UNPROCESSED),
    ]
    return click.Command(
        "task",
        callback=partial(task_cmd, path=path),
        context_settings=dict(allow_extra_args=True, ignore_unknown_options=True),
        params=params,
        short_help=meta.get("help-text"),
        help=meta.get("help-text"),
    )


def get_task_names(env):
    task_dir = get_task_dir(env)
    plugins_dir = get_plugins_dir(env)

    for dir_ in (task_dir, plugins_dir):
        if dir_.is_dir():
            for task_path in dir_.iterdir():
                if os.access(task_path, os.X_OK):
                    yield task_path.stem


def get_task_dir(env):
    if env.get("VG_TASKS_DIR"):
        return Path(env.get("VG_TASKS_DIR"))
    return Path(env["VG_APP_DIR"]) / "tasks"


def get_plugins_dir(env):
    if env.get("VG_PLUGINS_DIR"):
        return Path(env.get("VG_PLUGINS_DIR"))
    return Path(env["VG_APP_DIR"]) / ".vg-plugins"
