# vantage
A developer's build tool that cares for your environment.

## Install

    wget -qO- https://raw.githubusercontent.com/vantage-org/vantage/master/bootstrap | sh

Please read that script before you run the above command, check that you're happy with what it will do.

On systems with a `/etc/bash_completion.d/` directory a completion script will be installed. If you'd like to install it yourself you have to symlink the `complete` script into your completions directory, I like to link it to both `vantage` and `vg`.

### Dependencies

`vantage` is downloaded and updated using `git`, so you'll need that installed before the bootstrap script will work.

`vantage` is made up of bash scripts so you'll have to have that too. It doesn't have to be your current shell, it just has to be available. I've not tested `vantage` using non-bash shells, so your mileage may vary, please create an issue if you find something that doesn't work.

A small part of `vantage` uses perl, I don't think it will work without it. If you run into perl-related problems, please let me know and I'll what I can do about removing it as a dependency.

## Motivation

Config and sensitive data should be kept in the environment, not in code, and not in version control. Your app should be able to be dropped into a new machine with a new environment and pick up all the things it needs.

The problem always seemed to be in managing the environments I'm working in. There's production, staging, local dev, and testing, to name a few common ones. Some are more transitory than others; the local dev env can be torn down several times a day, the production env should only be touched if something really bad happens.

I want to be able to write down the various environments I'm working in and refer to them by name. So when I run a DB migration script I can run it once in the staging environment, and once in production, only changing my environment name between them.

I'm getting more and more into Docker and I'm learning how to apply it to my workflow. I particularly love how it enables me to treat services as transient. I can spin up a DB, make some stupid data inside it, then simply destroy the entire thing 5 mins later. Using `vantage` I can easily spin up different containers that have different environments.

What I want (and what I'm trying to build) is a tool for easily creating, destroying, and managing environments whilst I'm developing my app.

Also, I found it frustrating that different languages have completely different ways to manage and run scripts. I wanted something that was language agnostic, that I could use in all my projects and always have a pretty good idea of where to look for build scripts.

## Quick Tour

Here's a quick tour of installing and using `vantage`.

First, run the bootstrap script to install `vantage` into `/usr/local/vantage`. During installation symlinks to the script are placed in `/usr/local/bin`.

    $ wget -qO- https://raw.githubusercontent.com/vantage-org/vantage/master/bootstrap.sh | sh

Let's explore what's possible:

    $ vantage -h
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

    $ vantage -v VG_HW_NAME=Everyone hw
    Hello Everyone!

We can also put our environment in a file and refer to the file instead:

    $ echo "VG_HW_NAME=Me" > .env
    $ vantage -e .env hw
    Hello Me!

Now we could make several env files for each of our environments:

    $ mv .env local
    $ mkdir .env
    $ mv local .env/local
    $ echo "VG_HW_NAME=QA Team" > .env/staging
    $ echo "VG_HW_NAME=Everyone" > .env/production

And then easily switch between them:

    $ vantage -e .env/local hw
    Hello Me!
    $ vantage -e .env/staging hw
    Hello QA Team!
    $ vantage -e .env/production hw
    Hello Everyone!

Hopefully that's enough of a quick tour to give you the general idea. Create an issue if there's something that doesn't work or that doesn't make sense. Enjoy!

## What's Next?

Well, that's it for documentation really. `vantage` isn't a big project so you can easily skim through the files to see how things work and what things are possible.

`vantage` is built around the idea of using plugins to add new features. Take a look at the core and dogfood plugins that are in this repo to see how they work. They're pretty simple. You should build vantage plugins for your projects, perhaps to automate the deploy process, or run complex build steps.

There are some 'official' plugins that you'll find in the vantage-org GitHub organisation. They're a bit more involved but you might find them useful.

## Config

There are a couple of config values you can set. You can set them in your env files, or on the command line using the `-v` options. You can also save them into a special `.vantage` file in your app's root directory, this is the preferred method.

The `.vantage` file is a good place to keep machine specific config (e.g. absolute paths), this also means that you probably don't want to add it your version control.

### `VG_ENV_DIR`

Look for env files inside this directory, so you can refer to them by name, not path

    $ vantage hw
    Hello World!
    $ echo "VG_ENV_DIR=MACHINE_SPECIFIC_PATH/.env">>.vantage
    $ vantage -e staging hw
    Hello QA Team!

Now you're keeping all of your env in one directory, you can easily exclude everything from your version control.

### `VG_DEFAULT_ENV`

If this is set, always load config from this file, other named env files will overwrite config set here. I like to use this as my main, local, env file, it contains local database details, debug settings and nothing production-only. I then have staging and production files that can overwrite just the values they need to to function.

    $ vantage hw
    Hello World!
    $ echo "VG_DEFAULT_ENV=local">>.vantage
    $ vantage hw
    Hello Me!

### `VG_PLUGIN_PATH`

The absolute path of the directory that stores your own app's plugins.

This is the most useful one to set. You'll probably have a directory where you'll keep your scripts, this is how to tell vantage where they are.

    $ mkdir scripts
    $ echo "echo Hello Demo!" > scripts/demo
    $ chmod +x scripts/demo
    $ echo "VG_PLUGIN_PATH=MACHINE_SPECIFIC_PATH/scripts">>.vantage
    $ vantage demo
    Hello Demo!

### Read-Only

There are also config values that you should treat as read-only, they can be useful when writing your own plugins:

```
VG_APP_DIR - The absolute path to your app's directory (if known)
VG_ENV_FILE - The absolute path to the currently used env file, this is a temp file that is the final composition of all of the bits of environment
VG_INSTALL_DIR - The absolute path of where vantage has been installed
VG_NAMED_ENV - The name (or path) of the env file chosen using -e (if known)
VG_PARENT_ENV - The absolute path to the parent env file (if known), this is set if a vantage plugin calls another vantage plugin
VG_SHOW_HELP - Truthy if the user set the -h option
```

## Contributing

Please! Please do! Fork and PR to your heart's content. `vantage` was built very slowly in my spare time. I'm sure there are lots of bugs and lots of silly bits of code.

I'm very new to writing bash scripts so I'm certain that there are lots of improvements to be made style-wise.

If you can't contribute directly then please open an issue. Feature requests, bug reports, all kinds of things are welcome.

## Running the Tests

There's a plugin for it! Simply clone the project and run the tests plugin:

    $ git clone https://github.com/vantage-org/vantage.git
    $ cd vantage
    $ vantage tests

The above assumes that you have vantage already installed on your machine. If you'd prefer, you can use vagrant to spin up a development machine, there's a Vagrantfile in the repo.
