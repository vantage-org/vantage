import sys

import sh

from vantage import utils
from vantage.exceptions import VantageException


def shell_cmd(env, cmd, *args):
    utils.loquacious(f"Running system defined '{cmd}' inside env", env)
    utils.loquacious(f"  With args: {args}", env)
    try:
        command = sh.Command(cmd)
        command(
            *args,
            _env=env,
            _out=sys.stdout,
            _err=sys.stderr,
        )
    except sh.ErrorReturnCode as erc:
        utils.loquacious(f"  Exited with code {erc.exit_code}", env)
        sys.exit(erc.exit_code)
    except sh.CommandNotFound:
        raise VantageException(f"Command '{cmd}' not found")
