# Usage

## Quick Tour

Here's a quick tour of how to use vantage.

    $ vantage -h
    usage: vantage [-a PATH] [-e NAME ...] [-v KEY=[VALUE] ...] [--verbose] [-h] COMMAND...

    Run COMMAND inside a dynamic environment

    optional arguments:
    -a PATH, --app PATH   Set the app directory, the base dir from which every command is run
    -e NAME, --env NAME   Add an env file to the environment
    -v KEY[=VALUE], --var KEY[=VALUE]
                            Add a single variable to the environment
    --verbose             Print verbose debug messages to stdout
    -h, --help            Show this help message and exit

    builtin commands:
    __env      Manage environment variables and files
    __init     Initialise a vantage project
    __plugins  Manage vantage plugins
    __tasks    Lists all available tasks
    __version  Print current vantage version number

    See the GitHub repo for more details: https://github.com/vantage-org/vantage

From a fresh install with a blank project vantage doesn't do much beyond letting you run commands. Try this:

    $ vantage ls
    ...

As you can see, it just runs the `ls` command and does what you would expect it to.

Let's try:

    $ vantage env
    VG_APP_DIR=...
    VG_VERBOSE=

Here you can see that vantage has completely changed the environment variables for the command that you ran. The only 
ones here are some of the default vantage "internal" variables.

Let's use a vantage helper script to initialise a new project:

    $ mkdir testdrive
    $ cd testdrive
    $ vantage __init
    $ ls -a
    . .. .env .vantage

The init script has added a .env directory with a default environment in it. It's also added a .vantage file with some 
variables declared.

Let's add a variable to the default environment (using another helper script):

    $ vantage __env NAME=Alice

And see it appear in the env:

    $ vantage env
    NAME=Alice
    VG_APP_DIR=...
    VG_VERBOSE=

Let's create a new environment:

    $ vantage --env test __env NAME=Bob

And use the same command as above, but with the new environment:

    $ vantage -e test env
