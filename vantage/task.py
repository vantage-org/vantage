import sys
import os
from pathlib import Path

import sh
from ruamel.yaml import YAML

from vantage import utils
from vantage.exceptions import VantageException

yaml = YAML(typ="safe")


def execute_task_cmd(env, path, *args):
    utils.loquacious(f"Running task in {path}", env)
    utils.loquacious(f"  With args: {args}", env)
    meta = load_meta(env, path)
    env = update_env(env, meta)
    try:
        if meta.get("image"):
            utils.loquacious("  Spinning up docker image", env)
            utils.loquacious(f"  Path is: {os.environ.get('PATH')}", env)
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
            utils.loquacious("  Passing task over to sh", env)
            env["PATH"] = os.environ.get("PATH", "")
            cmd = sh.Command(str(path))
        utils.loquacious(f"Running command {cmd} with args {args}", env)
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
            f"  Something went wrong, returned exit code {erc.exit_code}", env
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


def load_meta(env, path):
    utils.loquacious("  Loading meta from task file", env)
    with path.open() as f:
        content = f.read()
        sep = None
        for line in content.splitlines():
            if "---" in line:
                sep = line
                break
        if sep is None:
            utils.loquacious("  No meta found", env)
            return {}
        else:
            _, meta, script = content.split(sep, 2)
            comment_marker = sep.replace("---", "")
            utils.loquacious(f"  Meta commented out using '{comment_marker}'", env)
            meta = meta.replace(f"\n{comment_marker}", "\n")
            return yaml.load(meta)


def update_env(env, meta):
    defaults = meta.get("environment")
    if defaults is not None:
        utils.loquacious("  Updating env with default environment in task meta", env)
        defaults = utils.get_env_from_key_val_list(defaults)
        for key, val in defaults:
            if key not in env:
                val = insert_env_vals(val, env)
                env[key] = val
                utils.loquacious(f"    {key}={val}", env)
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
        raise VantageException(f"The env file '{name_or_path}' does not exist")
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


def ensure_network(name):
    sh.docker("network", "create", name, _ok_code=[0, 1])
