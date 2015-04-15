# vantage
Command line shortcuts for managing Docker containers during development.

## Install

    wget -qO- https://raw.githubusercontent.com/WilliamMayor/vantage/master/bootstrap.sh | sh

## Motivation

I'm getting more and more into Docker and I'm learning how to apply it to my workflow. I particularly love how it enables me to treat services as transient. I can spin up a DB, make some stupid data inside it, then simply destroy the entire thing 5 mins later. Want to see what happens to the app if the DB gets corrupted? Try it, find out. Want to see what kind of destructive scripting is possible using your API? Go for it.

With this in mind I've been juggling some complicated spin up scripts. I have to take some environment variables and combine them with others, then pass them into the new container. I also want to link containers and mount volumes etc. etc. I'm certainly not running simple one liners.

What I want (and what I'm trying to build) is a tool for easily creating, destroying, and managing Docker containers whilst I'm developing my app.

## Current Builtin Functionality

    vantage help

Display the help page, including the help listings for any installed plugins.

    vantage update

Use git to update vantage from GitHub.

    vantage app:build

Builds the Docker app found at `VG_APP_DIR`, gives it a tag of `vg_app`. For example `VG_APP_DIR=/vagrant vantage app:build` is the same (as long as there are no overrides) as `docker build -t vg_app $VG_APP_DIR`

    vantage app:run

Runs the Docker app built using `vantage app:build`.

## Plugins

There is a bare minimum feature set baked into the vantage script itself. The majority of the features come from the plugin system. Some plugins (like `vantage app:*`) come with vantage, pre-installed. Some you can download and use. You can also build your own, to customise vantage for your specific project (take a look at the [https://github.com/WilliamMayor/vantage/tree/master/dogfood](dogfood) scripts to see how vantage is customised to develop vantage).

Plugins are directories with scripts inside. To find plugin directories vantage looks inside `/usr/local/vantage/plugins` then every directory listed in the `VG_PLUGIN_PATH` environment variable. Script files have the following names and meanings:

    commands

These are the main commands run by this plugin. The standard functionality. The builtin [https://github.com/WilliamMayor/vantage/tree/master/plugins/app](app) plugin uses `commands` to run some really simple Docker commands.

    override

Commands can be overridden by adding them to an `override` script. Only one override command will be run, no `pre` or `post` scripts, and certainly no `command`. Our [https://github.com/WilliamMayor/vantage/tree/master/dogfood](dogfood) plugins uses this feature to replace the standard `app:run` with an interactive version that calls `docker run -it`.

    pre

Commands in here will run before the standard command. This could be used to initialise dependencies before running a container.

    post

Commands here will be run after the standard command. This could be used to teardown a finished environment, or to add some extra build steps after the standard build has finished.
