# Structure

vantage is a python module, so it contains files with `.py` extensions (modules) and directories (packages) that contain
an `__init__.py` file as well as other modules.

At the top of the vantage package are these modules:

- `__main__.py`
- `entry.py`
- `exceptions.py`
- `shell.py`
- `task.py`
- `utils.py`

Then there's a package of builtin commands:

- `builtin/`
    - [`env.py`][vantage.builtin.env]
    - `init.py`
    - `plugins.py`
    - `tasks.py`
    - `version.py`
    
The `entry.py` file is the starting place for the tool. It takes in the arguments passed to it by the user and runs one
of the other modules/functions.
