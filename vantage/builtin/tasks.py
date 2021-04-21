from vantage import utils
from vantage.task import load_meta


def list_tasks_cmd(env, *args):
    utils.loquacious("Running __tasks command", env)

    print_names(env, utils.get_plugins_dir(env), "plugins")
    print_names(env, utils.get_task_dir(env), "project")


def print_names(env, dir_, name):
    if dir_.is_dir():
        tasks = sorted(get_tasks(env, dir_))
        if tasks:
            max_length = max(len(name) for name, _ in tasks)
            print(f"Tasks from {name} ({dir_}):")
            for name, path in tasks:
                meta = load_meta(env, path)
                help_text = meta.get("help-text", "")
                print(f"  {name.ljust(max_length)}  {help_text}")


def get_tasks(env, dir_):
    utils.loquacious(f"Listing tasks inside {dir_}", env)
    for task_path in dir_.iterdir():
        if utils.is_executable(task_path):
            yield task_path.stem, task_path
        elif task_path.is_dir():
            for sub_task, sub_path in get_tasks(env, task_path):
                yield f"{task_path.stem} {sub_task}", sub_path
