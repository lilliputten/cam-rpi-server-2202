#!/bin/sh
# @desc Check basic required variables
# @changed 2022.01.03, 16:37

if [ -z "$DIST_REPO" ]; then
  echo "Repository url isn't specified. See 'DIST_REPO' parameter in 'util-config.sh'"
  exit 1
fi
if [ -z "$PUBLISH_FOLDER" ]; then
  echo "Publish folder isn't specified. See 'PUBLISH_FOLDER' parameter in 'util-config.sh'"
  exit 1
fi
if [ ! -d "$PUBLISH_FOLDER" ]; then
  echo "No publish folder. Probably submodule was not initialized. Use script 'util-publish-init.sh'."
  exit 1
fi


