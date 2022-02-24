#!/bin/sh
# @module rpi-gunicorn-server-create-crontab-entry
# @desc Create crontab entry for automatic start of guncorn server (rpi).
# @since 2022.02.24, 03:52
# @changed 2022.02.24, 04:13
#
# @see https://stackoverflow.com/questions/610839/how-can-i-programmatically-create-a-new-cron-job

CRONTABCMD="crontab"

REALFILE=`realpath "$0"`
UTILDIR=`dirname "$REALFILE"`
ROOTDIR=`dirname "$UTILDIR"`

UTILCMDNAME="rpi-start-server.sh"

UTILCMD_LINE="@reboot sh $UTILDIR/$UTILCMDNAME"

# Reading current crontab content (m.b. `2>&1`) skipping 'no crontab' and previous lines with `UTILCMDNAME`...
CURRENT_CRONTAB=`crontab -l \
  | sed "s/no crontab for $(whoami)//" \
  | sed -z "s/[^\n]*$UTILCMDNAME[^\n]*\n//g"
`

# # DEBUG
# echo "Check loaded crontab:"
# echo "$CURRENT_CRONTAB"

# Append our command (`UTILCMD_LINE`) and update crontab...
echo "$CURRENT_CRONTAB
$UTILCMD_LINE" | $CRONTABCMD - \
  && echo "Succesfully updated crontab:" \
  && $CRONTABCMD -l
