#!/bin/sh
# @desc Update publish folder (prepare remote update)
# @since 2020.12.08, 13:44
# @changed 2021.12.30, 04:51

# Import config variables (expected variables `$DIST_REPO` and `$PUBLISH_FOLDER`)...
test -f "./utils/util-config.sh" && . "./utils/util-config.sh"
test -f "./utils/util-config-local.sh" && . "./utils/util-config-local.sh"

# Check basic required variables...
test -f "./utils/util-config-check.sh" && . "./utils/util-config-check.sh"

# if [ -z "$DIST_REPO" ]; then
#   echo "Repository url isn't specified. See 'DIST_REPO' parameter in 'util-config.sh'"
#   exit 1
# fi
# if [ -z "$PUBLISH_FOLDER" ]; then
#   echo "Publish folder isn't specified. See 'PUBLISH_FOLDER' parameter in 'util-config.sh'"
#   exit 1
# fi
# if [ ! -d "$PUBLISH_FOLDER" ]; then
#   echo "No publish folder. Probably submodule was not initialized. Use script 'util-publish-init.sh'."
#   exit 1
# fi

BUILD_FOLDER="build"

# Make build if absent
test -d "$BUILD_FOLDER" || npm run -s build || exit 1

TIMESTAMP=`cat build-timestamp.txt`
TIMETAG=`cat build-timetag.txt`
VERSION=`cat build-version.txt`

echo "Updating ($VERSION, $TIMESTAMP) publish folder '$PUBLISH_FOLDER' from build folder '$BUILD_FOLDER'..."


  # git pull && \
cd "$PUBLISH_FOLDER" && \
  pwd && \
  rm -Rf * && \
  cp -Rfu ../$BUILD_FOLDER/* . && \
  cd .. && \
  echo OK

  # cp -Rfu ../$BUILD_FOLDER/.[^.]* . && \
  # cp -Rfu ../$BUILD_FOLDER/.??* . && \



