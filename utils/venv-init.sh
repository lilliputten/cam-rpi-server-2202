#!/bin/sh
# @desc Initialize python venv
# @changed 2022.02.06, 23:33

if uname | grep -q "CYGWIN"; then
  cmd /C "utils\venv-init.cmd"
else
  # Global system requirements...
  pip install setuptools virtualenv
  # Create venv...
  python -m virtualenv -p "/usr/bin/python3.9" .venv
  # Activate venv
  . ./.venv/Scripts/activate
  # Install project dependencies...
  pip install -r requirements-dev.txt
  # User info...
  echo "Use next command to activate venv: '. ./.venv/Scripts/activate'"
fi
