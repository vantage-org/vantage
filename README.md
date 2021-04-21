# vantage
A developer's build tool/task runner that cares for your environment.

vantage will run the command you give it with environment variables set as you need them. Turning complex commands into re-usable "task" scripts is easy. Switching between environments and running those tasks is easy too. Running tasks inside docker containers is what vantage does best.

## Install

Download the latest release from GitHub and untar/unzip it. There's an `install.sh` script in there that will show you a fairly standard way to install vantage.

It's a fairly plain install process, you download the binaries somewhere, then put a symlink to them on your PATH. We like to keep vantage installed in `/usr/local/vantage` and we symlink `/usr/local/vantage/vantage` to `/usr/local/bin/vantage` and `/usr/local/bin/vg`.

## Motivation

Config and sensitive data should be kept in the environment, not in code, and not in version control. Your app should be able to be dropped into a new machine with a new environment and pick up all the things it needs.

The problem always seemed to be in managing the environments I'm working in. There's production, staging, local dev, and testing, to name a few common ones. Some are more transitory than others; the local dev env can be torn down several times a day, the production env should only be touched if something really bad happens.

I want to be able to write down the various environments I'm working in and refer to them by name. So when I run a DB migration script I can run it once in the staging environment, and once in production, only changing my environment name between them.

I'm getting more and more into Docker and I'm learning how to apply it to my workflow. I particularly love how it enables me to treat services as transient. I can spin up a DB, make some stupid data inside it, then simply destroy the entire thing 5 mins later. Using vantage I can easily spin up different containers that have different environments.

What I want (and what I'm trying to build) is a tool for easily creating, destroying, and managing environments whilst I'm developing my app.

Also, I found it frustrating that different languages have completely different ways to manage and run scripts. I wanted something that was language agnostic, that I could use in all my projects and always have a pretty good idea of where to look for build scripts.

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

Here you can see that vantage has completely changed the environment variables for the command that you ran. The only ones here are some of the default vantage "internal" variables.

Let's use a vantage helper script to initialise a new project:

    $ mkdir testdrive
    $ cd testdrive
    $ vantage __init
    $ ls -a
    . .. .env .vantage

The init script has added a .env directory with a default environment in it. It's also added a .vantage file with some variables declared.

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

## Contributing

Please! Please do! Fork and PR to your heart's content. vantage was built very slowly in my spare time. I'm sure there are lots of bugs and lots of silly bits of code.

If you can't contribute directly then please open an issue. Feature requests, bug reports, all kinds of things are welcome.
