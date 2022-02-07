#!/bin/sh
# @desc Update/restart server on local device server (rpi)
# @since 2022.02.07, 20:41
# @changed 2022.02.07, 20:41

# Import config variables (expected variables `$DIST_REPO` and `$PUBLISH_FOLDER`)...
test -f "./utils/config.sh" && . "./utils/config.sh"
test -f "./utils/config-local.sh" && . "./utils/config-local.sh"

git pull

# TODO: Update/restart flask server
