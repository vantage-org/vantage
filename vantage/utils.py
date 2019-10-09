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


@click.pass_obj
def loquacious(env, line):
    if env is not None and env.get("VG_VERBOSE"):
        click.echo(f"VG-LOG: {line}")
