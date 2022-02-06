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

# # Check basic required variables...
# test -f "./utils/util-config-check.sh" && . "./utils/util-config-check.sh"

if [ -z "$DIST_REPO" ]; then
  echo "Repository url isn't specified. See 'DIST_REPO' parameter in 'util-config.sh'"
  exit 1
fi
if [ -z "$PUBLISH_FOLDER" ]; then
  echo "Publish folder isn't specified. See 'PUBLISH_FOLDER' parameter in 'util-config.sh'"
  exit 1
fi

if [ -d "$PUBLISH_FOLDER" ]; then
  echo "Publish folder already exists!"
  echo "Remove it first for re-initializing using command:"
  echo "'rm -Rf "$PUBLISH_FOLDER" .gitmodules ".git/modules/$PUBLISH_FOLDER"'."
  exit # Successfull exit
  # exit 1 # Exit with error code
  # echo "Uninstalling submodule..." # Alterative behavior
  # rm -Rf "$PUBLISH_FOLDER" .gitmodules
fi

echo "Initializing publish folder & submodule for '$PUBLISH_FOLDER'..."

echo "Init publish submodule with $DIST_REPO ..."
touch .gitmodules && \
  git submodule add -f "$DIST_REPO" "$PUBLISH_FOLDER" && \
  git rm --cached -f "$PUBLISH_FOLDER" .gitmodules && \
  test ! -z "$DIST_BRANCH" && ( \
    echo "Switch to branch '$DIST_BRANCH' ..." && \
    cd "$PUBLISH_FOLDER" && \
    git checkout "$DIST_BRANCH" && \
    cd .. \
  ) && \
  echo OK
