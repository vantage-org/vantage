# vantage
Command line shortcuts for managing Docker containers during development.

## Install

    wget -qO- https://raw.githubusercontent.com/WilliamMayor/vantage/master/bootstrap.sh | sh

## Motivation

I'm getting more and more into Docker and I'm learning how to apply it to my workflow. I particularly love how it enables me to treat services as transient. I can spin up a DB, make some stupid data inside it, then simply destroy the entire thing 5 mins later. Want to see what happens to the app if the DB gets corrupted? Try it, find out. Want to see what kind of destructive scripting is possible using your API? Go for it.

With this in mind I've been juggling some complicated spin up scripts. I have to take some environment variables and combine them with others, then pass them into the new container. I also want to link containers and mount volumes etc. etc. I'm certainly not running simple one liners.

What I want (and what I'm trying to build) is a tool for easily creating, destroying, and managing Docker containers whilst I'm developing my app.

## Current Functionality

    vantage help

Display the help page, including the help listings for any installed plugins.

    vantage update

Use git to update vantage from GitHub.
