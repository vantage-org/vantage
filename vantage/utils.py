import os
import base64
import binascii
import io
import json
import tarfile
import urllib.request
from pathlib import Path

import certifi

from vantage.exceptions import VantageException


def to_base64(value):
    value = base64.urlsafe_b64encode(value.encode("utf-8")).decode("utf-8")
    return f"base64:{value}"


def from_base64(value):
    if value.startswith("base64:"):
        try:
            value = base64.urlsafe_b64decode(value[7:]).decode("utf-8")
        except binascii.Error:
            pass
    return value


def loquacious(line, env):
    if env.get("VG_VERBOSE"):
        print(f"VG-LOG: {line}")


def load_env_from_file(path, ignore_missing=False):
    env = {}
    try:
        with path.open() as fp:
            for line in fp:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    value = from_base64(value.strip())
                    env[key.strip()] = value
    except FileNotFoundError:
        if not ignore_missing:
            raise VantageException(f"The env file '{path}' does not exist")
    return env


def determine_github_latest_release(name):
    certs = certifi.where()
    latest_release = urllib.request.urlopen(
        f"https://api.github.com/repos/vantage-org/{name}/releases/latest",
        cafile=certs,
    )
    latest_release = json.load(latest_release)
    for asset in latest_release["assets"]:
        if name in asset["name"]:
            return asset


def download_tarball(url, path):
    certs = certifi.where()
    archive = urllib.request.urlopen(url, cafile=certs)
    archive = urllib.request.urlopen(url, cafile=certs)
    archive = io.BytesIO(archive.read())
    tar = tarfile.open(fileobj=archive, mode="r:*")
    tar.extractall(path=path)


def is_executable(path):
    return path.is_file() and os.access(path, os.X_OK)


def get_task_dir(env):
    if env.get("VG_TASKS_DIR"):
        return Path(env.get("VG_TASKS_DIR"))
    return Path(env["VG_APP_DIR"]) / "tasks"


def get_plugins_dir(env):
    if env.get("VG_PLUGINS_DIR"):
        return Path(env.get("VG_PLUGINS_DIR"))
    return Path(env["VG_APP_DIR"]) / ".vg-plugins"


def get_env_from_key_val_list(key_vals):
    for key_val in key_vals:
        if "=" in key_val:
            key, val = key_val.split("=", 1)
            key = key.strip()
        else:
            key = key_val.strip()
            val = os.environ.get(key, "")
        val = from_base64(val.strip())
        yield key, val
