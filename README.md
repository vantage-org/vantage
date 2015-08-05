# vantage
Command line shortcuts for managing Docker containers during development.

## Install

    wget -qO- https://raw.githubusercontent.com/WilliamMayor/vantage/master/bootstrap | sh

`vantage` is downloaded and updated using git, so you'll need that installed before the bootstrap script will work.

You'll probably want Docker installed too.

## Motivation

I'm getting more and more into Docker and I'm learning how to apply it to my workflow. I particularly love how it enables me to treat services as transient. I can spin up a DB, make some stupid data inside it, then simply destroy the entire thing 5 mins later. Want to see what happens to the app if the DB gets corrupted? Try it, find out. Want to see what kind of destructive scripting is possible using your API? Go for it.

With this in mind I've been juggling some complicated spin up scripts. I have to take some environment variables and combine them with others, then pass them into the new container. I also want to link containers and mount volumes etc. etc. I'm certainly not running simple one liners.

What I want (and what I'm trying to build) is a tool for easily creating, destroying, and managing Docker containers whilst I'm developing my app.

## Quick Tour

Here's a quick tour of installing and using `vantage`. I use Vagrant, so some of the paths are Vagrant-box specific.

First, run the bootstrap script to install `vantage` into `/usr/local/vantage`. During installation symlinks to the script are placed in `/usr/local/bin`. Then set some environment variables so `vantage` knows where to find things. `VG_PLUGIN_PATH` is treated a bit like `PATH` in that you can add multiple locations to it, separating each with  a `:`. `vantage` comes with some plugins already, more can be downloaded and you are encouraged to build your own, project-specific, ones too. `VG_APP_DIR` is used by `vantage app build` to find your project and build its Docker container.

    $ wget -qO- https://raw.githubusercontent.com/WilliamMayor/vantage/master/bootstrap.sh | sh
    ...
    $ export VG_PLUGIN_PATH=/vagrant/vantage:/usr/local/vantage-other
    $ export VG_APP_DIR=/vagrant

Let's explore what's possible:

    $ vg help
    Usage: vantage [--env|-e ENV_FILE [...]] COMMAND [OPTIONS]

    Commands:
        help - Print the list of commands
        app build - Build your app
        app run - Spin up your app
        update - Update vantage

We can build our project using:

    $ vg app build
    Sending build context to Docker daemon 145.4 kB
    ...
    Successfully built 6c66dbcb2f61

Then run it:

    $ vg app run
    Hello, world!

Now let's run the app using a different environment:

    $ vim .env
    NAME=Helen
    $ vg --env .env app run
    Hello, Helen!

We can set that env file to be the default one:

    $ export VG_DEFAULT_ENV=/vagrant/.env
    $ vg app run
    Hello, Helen!

And then combine our default env with a different one:

    $ vim .other_env
    GREETING=Salut
    $ vg --env .other_env app run
    Salut, Helen!

The functionality's a little bare, let's add our own plugin:

    $ mkdir -p /vagrnat/vantage/app
    $ vim /vagrant/vantage/app/override
    #!/usr/bin/env bash
    set -eo pipefail
    shopt -s nullglob

    case "$1" in
        run)
            docker run \
                --env-file "$VG_ENV_FILE" \
                --interactive \
                --tty \
                vg_app bash
            exit $VG_VALID_EXIT
            ;;
        help)
            echo "    app run - (override) Run an interactive shell"
            ;;
        *)
            exit $VG_NOT_IMPLEMENTED_EXIT
            ;;
    esac
    $ chmod +x /vagrant/vantage/app/override
    $ vg help
    Usage: vantage [--env|-e ENV_FILE [...]] COMMAND [OPTIONS]

    Commands:
        help - Print the list of commands
        app build - Build your app
        app run - Spin up your app
        update - Update vantage
        app run - (override) Run an interactive shell
    $ vg app run
    root@08e51e548957:/usr/src/app# ...

We created an override script this time, it replaced the previous `vg app run` command. We can also create `pre`, `post`, and `commands` scripts (or combinations of those) to customise our plugins.
