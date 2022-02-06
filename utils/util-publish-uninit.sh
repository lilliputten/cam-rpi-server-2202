#!/bin/sh
# @desc Initialize publish syncing repository
# @changed 2021.01.17, 19:53

# NOTE: For uninstall/reinitialize publish submodule, use:
# ```shell
# rm -Rf publish .gitmodules .git/modules/publish
# ```

# Import config variables (expected variables `$DIST_REPO` and `$PUBLISH_FOLDER`)...
test -f "./utils/util-config.sh" && . "./utils/util-config.sh"
test -f "./utils/util-config-local.sh" && . "./utils/util-config-local.sh"

# Check basic required variables...
test -f "./utils/util-config-check.sh" && . "./utils/util-config-check.sh"

if [ -z "$PUBLISH_FOLDER" ]; then
  echo "Publish folder isn't specified. See 'PUBLISH_FOLDER' parameter in 'util-config.sh'"
  exit 1
fi

echo "Uninitializing publish folder & submodule for '$PUBLISH_FOLDER'..."

rm -Rf "$PUBLISH_FOLDER" .gitmodules ".git/modules/$PUBLISH_FOLDER" && \
  echo Ok
