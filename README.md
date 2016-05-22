# vantage
A developer's build tool that cares about your environment.

## Install

    wget -qO- https://raw.githubusercontent.com/vantage-org/vantage/master/bootstrap | sh

`vantage` is downloaded and updated using git, so you'll need that installed before the bootstrap script will work.

## Motivation

Config and sensitive data should be kept in the environment. Your app should be able to be dropped into a new machine with a new environment and pick up all the things it needs. This is one of the 12-factors.

The problem always seemed to be in managing the environments I'm working in. There's production, staging, local dev, and testing, to name a few common ones. Some are more transitory than others; the local dev env can be torn down several times a day, the production env should only be touched if something really bad happens.

I want to be able to write down the various environments I'm working in and refer to them by name. So when I run a DB migration script I can run it once in the staging environment, and once in production, only changing my environment name between them.

I'm getting more and more into Docker and I'm learning how to apply it to my workflow. I particularly love how it enables me to treat services as transient. I can spin up a DB, make some stupid data inside it, then simply destroy the entire thing 5 mins later. Using `vantage` I can easily spin up different containers that have different environments.

What I want (and what I'm trying to build) is a tool for easily creating, destroying, and managing environments whilst I'm developing my app.

## Quick Tour

Here's a quick tour of installing and using `vantage`.

First, run the bootstrap script to install `vantage` into `/usr/local/vantage`. During installation symlinks to the script are placed in `/usr/local/bin`.

    $ wget -qO- https://raw.githubusercontent.com/vantage-org/vantage/master/bootstrap.sh | sh

Let's explore what's possible:

    $ vg -h
    usage: vantage [-h] [-a APP_DIR] [-e ENV_FILE]... [-v KEY=VALUE]... COMMAND

        -h - Show the help text for COMMAND (if it is a vantage plugin)
        -a - Set the app directory
        -e - Add an env file to the environment
        -v - Add a single variable to the environment

    Commands:
        __env - Read and write your app's environment values
        __plugins - Manage vantage plugins
        __update - Update vantage and it's plugins
        * - Any other command at all

    See the GitHub repo for more details (https://github.com/vantage-org/vantage)

You can use the `-h` flag to learn more about each command. Before you customise `vantage` to your own project, the default installation comes with some 'dogfood' plugins that we can use now to explore how things work:

    $ vantage hw
    Hello World!

Let's set an environment variable to change the name:

    $ vantage --var VG_HW_NAME=Everyone hw
    Hello Everyone!

We can also put our environment in a file and refer to the file instead:

    $ echo "VG_HW_NAME=Everyone" > .env
    $ vantage --env .env hw
    Hello Everyone!

We can also set the env in the `.vantage` file:

    $ echo "VG_HW_GREETING=Salut" > .vantage
    $ vantage hw
    Salut World!

And we can use the `.vantage` file to set a default environment:

    $ echo "VG_DEFAULT_ENV=.env" >> .vantage
    $ vantage hw
    Salut Everyone!

## What's Next?

Well, that's it for documentation really. `vantage` isn't a big project so you can easily skim through the files to see how things work and what things are possible.

`vantage` is built around the idea of using plugins to add new features. Take a look at the core and dogfood plugins that are in this repo to see how they work. They're pretty simple. You should build vantage plugins for your projects, perhaps to automate the deploy process, or run complex build steps.

There are some 'official' plugins that you'll find in the vantage-org GitHub organisation. They're a bit more involved but you might find them useful.

## Contributing

Please! Please do! Fork and PR to your heart's content. `vantage` was built very slowly in my spare time. I'm sure there are lots of bugs and lots of silly bits of code.

If you can't contribute directly then please open an issue. Feature requests, bug reports, all kinds of things are welcome.
