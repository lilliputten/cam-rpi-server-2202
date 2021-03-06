#!/bin/sh
# @desc Create/update version tag (from build folder)
# @since 2020.12.30, 20:24
# @changed 2022.01.03, 19:58

# Import config variables (expected variables `$DIST_REPO` and `$PUBLISH_FOLDER`)...
test -f "./utils/config.sh" && . "./utils/config.sh"
test -f "./utils/config-local.sh" && . "./utils/config-local.sh"

if [ -z "$SRC_TAG_PREFIX" ]; then
  echo "No tag prefix is specified. Add 'SRC_TAG_PREFIX' parameter in 'config.sh'."
  exit 1
fi

VERSIONFILE="build-version.txt"
if [ ! -f "$VERSIONFILE" ]; then
  echo "No version file ($VERSIONFILE) exist!"
  exit 1
fi

VERSION=`cat "$VERSIONFILE"`

echo "Create/update tag $SRC_TAG_PREFIX.$VERSION..." \
  && git tag -f "$SRC_TAG_PREFIX.$VERSION" \
  && git push origin -f --tags \
  && echo "OK"
