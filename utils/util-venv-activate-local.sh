#!/bin/sh
# @changed 2022.02.06, 23:33

if uname | grep -q "CYGWIN"; then
  cmd /C "utils\util-venv-activate-local.cmd"
else
  source "./.venv/Scripts/activate"
fi
