from pathlib import Path

import click

from vantage import utils


@click.command(name="__init")
@click.pass_obj
def init(env):
    """Initialise the VG_APP_DIR with default vantage config"""
    utils.loquacious("Running __init")
    app_dir = Path(env["VG_APP_DIR"])
    vg_file = app_dir / ".vantage"
    if not vg_file.exists():
        with vg_file.open(mode="w") as fp:
            fp.write(f"VG_TASKS_DIR={app_dir / 'tasks'}\n")
            fp.write(f"VG_PLUGINS_DIR={app_dir / '.vg-plugins'}\n")
            fp.write(f"VG_ENV_DIR={app_dir / '.env'}\n")
            fp.write("VG_DEFAULT_ENV=default\n")
    env_dir = app_dir / ".env"
    env_dir.mkdir(exist_ok=True)
    env_file = env_dir / "default"
    env_file.touch(exist_ok=True)
