import sys
import os
import subprocess
from pathlib import Path

import strictyaml

from vantage import utils
from vantage.exceptions import VantageException


def execute_task_cmd(env, path, *args):
    utils.loquacious(f"Running task in {path}", env)
    utils.loquacious(f"  PATH is: {os.environ.get('PATH')}", env)
    utils.loquacious(f"  With args: {args}", env)
    meta = load_meta(env, path)
    env = update_env(env, meta)
    if meta.get("image"):
        utils.loquacious("  Spinning up docker image", env)
        image = meta.get("image")
        docker = utils.find_executable("docker")
        if docker is None:
            raise VantageException(f"Couldn't find docker in PATH")
        run_args = [
            docker,
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
                elif v == "true":
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
        run_args += [tag, "/vg-task", *args]
        run_subprocess(*run_args, env=env)
    else:
        utils.loquacious("  Passing task over to subprocess", env)
        env["PATH"] = os.environ.get("PATH", "")
        run_subprocess(str(path), *args, env=env)


def run_subprocess(*args, env):
    utils.loquacious(f"Running command {args[0]} with args {args[1:]}", env)
    completed = subprocess.run(
        list(args),
        env=env,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    utils.loquacious(f"  Exited with code {completed.returncode}", env)
    sys.exit(completed.returncode)


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
            return strictyaml.load(meta).data


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
    subprocess.run(
        ["docker", "network", "create", name],
    )
