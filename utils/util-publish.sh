#!/bin/sh
# @desc Publish (and make if absent) publish build
# @changed 2022.01.04, 01:08

# Import config variables (expected variables `$DIST_REPO` and `$PUBLISH_FOLDER`)...
test -f "./utils/util-config.sh" && . "./utils/util-config.sh"
test -f "./utils/util-config-local.sh" && . "./utils/util-config-local.sh"

# Check basic required variables...
test -f "./utils/util-config-check.sh" && . "./utils/util-config-check.sh"

# Make build if absent
sh "./utils/util-publish-update.sh" || exit 1

TIMESTAMP=`cat build-timestamp.txt`
TIMETAG=`cat build-timetag.txt`
VERSION=`cat build-version.txt`

echo "Publishing build ($VERSION, $TIMESTAMP)..."

# TODO: Compare actual and previously published versions? (The git is checking for changes itself anyway.)

COMMIT_TEXT="Build $DIST_BRANCH.$VERSION, $TIMESTAMP ($TIMETAG)"
# echo "Fetch..." && git fetch && git pull && \
cd "$PUBLISH_FOLDER" && \
  echo "Fetch..." && git fetch && git pull -Xours && \
  echo "Add files..." && git add . -Av && \
  echo "Commit..." && git commit -am "$COMMIT_TEXT" && \
  echo "Push basic branch..." && git push && \
  echo "Done" && cd ..
  # echo "Don't forget to update version for target project dependency (package.json, WebUiCore entry)"

  # echo "Create/update tag $DIST_BRANCH.$VERSION..." && git tag -f -am "$COMMIT_TEXT" "$DIST_BRANCH.$VERSION" && \
  # echo "Push tagged branch with tags..." && git push -f --tags && \

  # ( ( ( git tag | grep -q "v$VERSION" ) && echo "Tag exist: update" && git tag -d "v$VERSION" ) || echo "Tag absent: create" ) &&
  # ( git tag "v$VERSION" || echo "Tag already exists" ) && \

