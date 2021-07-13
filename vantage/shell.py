import sys
import subprocess

from vantage import utils
from vantage.exceptions import VantageException


def shell_cmd(env, cmd, *args):
    utils.loquacious(f"Running system defined '{cmd}' inside env", env)
    utils.loquacious(f"  With args: {args}", env)

    try:
        cmd = utils.find_executable(cmd)
        if cmd is None:
            raise FileNotFoundError()
        completed = subprocess.run(
            [cmd, *args],
            env=env,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        utils.loquacious(f"  Exited with code {completed.returncode}", env)
        return completed.returncode
    except FileNotFoundError:
        raise VantageException(f"Command '{cmd}' not found")
