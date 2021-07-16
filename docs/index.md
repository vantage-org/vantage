# Home

vantage is a developer's build tool/task runner that cares for your environment.

vantage will run the command you give it with environment variables set as you need them. Turning complex commands into
re-usable "task" scripts is easy. Switching between environments and running those tasks is easy too. Running tasks 
inside docker containers is what vantage does best.

## Motivation

Config and sensitive data should be kept in the environment, not in code, and not in version control. Your app should be
able to be dropped into a new machine with a new environment and pick up all the things it needs.

The problem always seemed to be in managing the environments I'm working in. There's production, staging, local dev, and
testing, to name a few common ones. Some are more transitory than others; the local dev env can be torn down several 
times a day, the production env will probably only be changed rarely.

I want to be able to write down the various environments I'm working in and refer to them by name. So when I run a DB 
migration script I can run it once in the staging environment, and once in production, only changing my environment name
between them.

I'm getting more and more into Docker and I'm learning how to apply it to my workflow. I particularly love how it enables
me to treat services as transient. I can spin up a DB, make some stupid data inside it, then simply destroy the entire 
thing 5 mins later. Using vantage I can easily spin up different containers that have different environments.

What I want (and what I'm trying to build) is a tool for easily creating, destroying, and managing environments whilst 
I'm developing my app.

Also, I found it frustrating that different languages have completely different ways to manage and run scripts. I wanted
something that was language agnostic, that I could use in all my projects and always have a pretty good idea of where to
look for build scripts.
