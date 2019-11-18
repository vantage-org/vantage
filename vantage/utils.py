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
