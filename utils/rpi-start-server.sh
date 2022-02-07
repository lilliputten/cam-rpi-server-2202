#!/bin/sh
# @desc Update/restart server on local device server (rpi)
# @since 2022.02.07, 22:01
# @changed 2022.02.07, 23:31
# @see https://peppe8o.com/beginners-guide-to-install-a-flask-python-web-server-on-raspberry-pi/
# @see https://docs.gunicorn.org/en/stable/run.html
# @see utils/rpi-gunicorn-help.txt

# Full path to gunicorn python script (for running under crontab; use `command -v gunicorn`)
GUNICORN="/home/pi/.local/bin/gunicorn"

# Determine real project path...
REALFILE=`realpath "$0"`
REALDIR=`dirname "$REALFILE"`
ROOT=`dirname "$REALDIR"`

# # Import config variables (expected variables `$DIST_REPO` and `$PUBLISH_FOLDER`)...
# test -f "$REALDIR/utils/config.sh" && . "$REALDIR/utils/config.sh"
# test -f "$REALDIR/utils/config-local.sh" && . "$REALDIR/utils/config-local.sh"

echo "Starting server in folder: $ROOT" # (via $REALFILE)"

# Is running instance exists?
if [ -f "$ROOT/.gunicorn.pid" ]; then
  PID=`cat "$ROOT/.gunicorn.pid"`
  echo "Found running instance with pid '$PID'. Trying to stop it."
  kill $PID
  # NOTE: You can use:
  # `ps -e | grep gunicorn`
  # `pkill gunicorn`
  # `killall gunicorn`
fi

# Remove all log files...
rm -f "$ROOT/log*.txt" "$ROOT/.gunicorn.*"

# Start daemon...
echo "Starting daemon..." \
&& "$GUNICORN" \
  --reload \
  -D \
  -w 1 \
  -b 0.0.0.0:4000 \
  --chdir "$ROOT" \
  --pid="$ROOT/.gunicorn.pid" \
  --log-file="$ROOT/.gunicorn.log" \
  index \
&& echo OK

# TODO: Extract port number (and other options?) to config?
