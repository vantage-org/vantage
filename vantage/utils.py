import binascii
import base64

import click


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


def loquacious(line, env=None):
    try:
        env = env or click.get_current_context().obj
        if env is not None and env.get("VG_VERBOSE"):
            click.echo(f"VG-LOG: {line}")
    except RuntimeError:
        # This happens when there's no active click context so we can't get the
        # env. In this case we default to not printing the verbose logs.
        # This situation happens when you're trying to autocomplete
        pass


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
            raise click.ClickException(f"The env file '{path}' does not exist")
    return env
