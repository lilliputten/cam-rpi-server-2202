#!/bin/sh
# @module utils/rpi-gunicorn-server-create.sh
# @desc Create systemd service for control guncorn server (rpi).
# @since 2022.02.24, 02:45
# @changed 2022.02.24, 02:57
#
# @see https://bartsimons.me/gunicorn-as-a-systemd-service/

  # && sudo cp "./utils/$SERVICE_FILE" "$SYSTEMD_FOLDER" \
SERVICE_FILE="rpi-gunicorn-server.service"
SYSTEMD_FOLDER="/lib/systemd/system"
SYSTEMD_FILE="$SYSTEMD_FOLDER/$SERVICE_FILE"

# Check service file exists...
if [ -f "$SYSTEMD_FILE" ]; then
  echo "Service file '$SYSTEMD_FILE' already exists." \
  && echo "Try to remove it before re-creating with commands:" \
  && echo "Use 'sudo systemctl stop $SERVICE_FILE' to stop service." \
  && echo "Use 'sudo systemctl disable $SERVICE_FILE' to remove service." \
  && echo "Use 'sudo rm $SYSTEMD_FOLDER/$SERVICE_FILE' to remove service file link." \
  && exit 1
fi

echo "Creating service '$SERVICE_FILE' in folder '$SYSTEMD_FOLDER'..." \
  && sudo ln "./utils/$SERVICE_FILE" "$SYSTEMD_FILE" \
  && echo "Created service file (with link)." \
  && sudo systemctl daemon-reload \
  && echo "Reloaded systemctl daemon-reload." \
  && sudo systemctl enable "$SERVICE_FILE" \
  && echo "Enabled '$SERVICE_FILE'. Checking operation result (expecting '...enabled' string below):" \
  && sudo systemctl list-unit-files | grep "$SERVICE_FILE" \
  && echo "Use 'sudo systemctl start $SERVICE_FILE' to start service." \
  && echo "Use 'sudo systemctl stop $SERVICE_FILE' to stop service." \
  && echo "Use 'sudo systemctl disable $SERVICE_FILE' to disable service." \
  && echo "Use 'sudo systemctl enable $SERVICE_FILE' to re-enable service." \
  && echo "Use 'sudo rm $SYSTEMD_FOLDER/$SERVICE_FILE' to remove service file link." \
  && echo "Use 'sudo systemctl list-unit-files | grep $SERVICE_FILE' to control service file state (enabled/disabled)." \
  && echo "Use 'sudo systemctl list-units --type=service --all | grep $SERVICE_FILE' to control service state (loaded/active/inactive/running/dead etc)." \
  && echo "Done."
