import sys
import argparse
from pathlib import Path

from vantage import utils
from vantage.exceptions import VantageException

parser = argparse.ArgumentParser(
    prog="vantage __env",
    description="Manage environment variables and files",
    allow_abbrev=False,
)
parser.add_argument(
    "-b",
    "--base64",
    action="store_true",
    help="When setting a var convert it to base64 first",
)
parser.add_argument(
    "-s",
    "--stdin",
    action="store_true",
    help="When setting a var read the value from stdin",
)
parser.add_argument(
    "key_val",
    nargs="?",
    help="A KEY=VALUE pair to save to an env file",
)


def env_cmd(env, *args):
    utils.loquacious("Running __env", env)
    args = parser.parse_args(args)

    if args.key_val is None:
        utils.loquacious("  Printing ENV", env)
        for k, v in env.items():
            print(f"{k}={v}")
    elif "=" in args.key_val:
        utils.loquacious("  Setting ENV value", env)
        key, val = args.key_val.split("=", 1)
        write_env_value(env, key, val, args.base64)
    elif args.stdin:
        utils.loquacious("  Setting ENV value from stdin", env)
        val = sys.stdin.read().strip()
        write_env_value(env, args.key_val, val, args.base64)
    else:
        utils.loquacious("  Printing single ENV value", env)
        try:
            value = env[args.key_val]
            print(value)
        except KeyError:
            raise VantageException(f"No value found for '{args.key_val}'")


def write_env_value(env, key, value, base64=False):
    try:
        env_file = Path(env["VG_ENV_FILE"])
        utils.loquacious(f"  Adding {key}={value} to {env_file}", env)
        if base64:
            value = utils.to_base64(value)
        env[key] = value
        with env_file.open("w") as fp:
            for key, value in sorted(env.items()):
                if not key.startswith("VG_"):
                    fp.write(f"{key}={value}\n")
    except KeyError:
        raise VantageException(
            "No env file provided, there's nowhere to store this value"
        )
