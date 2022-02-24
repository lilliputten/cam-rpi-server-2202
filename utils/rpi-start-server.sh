#!/bin/sh
# @module rpi-start-server.sh
# @desc Update/restart server on local device server (rpi).
# @since 2022.02.07, 22:01
# @changed 2022.02.24, 04:37
#
# Script may be called from command line directly or under crontab. See crrsp sections in README.md file.
#
# @see https://peppe8o.com/beginners-guide-to-install-a-flask-python-web-server-on-raspberry-pi/
# @see https://docs.gunicorn.org/en/stable/run.html
# @see utils/rpi-gunicorn-help.txt

# Full path to gunicorn python script (for running under crontab; use `command -v gunicorn`)
GUNICORN="/home/pi/.local/bin/gunicorn"

# Determine real project path (is required for crontab execution)...
REALFILE=`realpath "$0"`
UTILSDIR=`dirname "$REALFILE"`
ROOTDIR=`dirname "$UTILSDIR"`

PIDFILE="$ROOTDIR/log-gunicorn.pid"
LOGFILE="$ROOTDIR/log-gunicorn.log"

# # Import config variables (expected variables `$DIST_REPO` and `$PUBLISH_FOLDER`)...
# test -f "$UTILSDIR/config.sh" && . "$UTILSDIR/config.sh"
# test -f "$UTILSDIR/config-local.sh" && . "$UTILSDIR/config-local.sh"

echo "Starting server in folder: $ROOTDIR" # (via $REALFILE)"

# Is running instance exists?
if [ -f "$PIDFILE" ]; then
  PID=`cat "$PIDFILE"`
  echo -n "Found running instance with pid $PID, trying to stop it... "
  if kill $PID > /dev/null 2>&1; then
    echo "Ok."
  else
    echo "Error (may be the pid from the previous session have been left)."
  fi
  # NOTE: You can also use:
  # `ps -e | grep gunicorn`
  # `pkill gunicorn`
  # `killall gunicorn`
fi

# # Remove old log files...
rm -f "$PIDFILE"
# # "$ROOTDIR/log*.txt" # NOTE: Remove log files?

# Start daemon...
echo -n "Starting daemon... " \
&& sleep 1 \
&& echo "" >> "$LOGFILE" \
&& "$GUNICORN" \
  --reload \
  -D \
  -w 1 \
  -b 0.0.0.0:4000 \
  --chdir "$ROOTDIR" \
  --pid="$PIDFILE" \
  --log-file="$LOGFILE" \
  index \
&& echo "Done." \
&& echo -n "Waiting for pid file ($PIDFILE)..." \
&& while ! test -f "$PIDFILE"; do echo -n " ." && sleep 1; done \
&& echo " Got pid: `cat $PIDFILE`."

# TODO: Extract port number (and other options?) to config?
