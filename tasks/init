#!/bin/sh
# ---
# help-text: Initialise the project, create a venv and install deps
# ---
if [ ! -d venv ]
then
  python3 -m venv venv
fi

. venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install -e .
