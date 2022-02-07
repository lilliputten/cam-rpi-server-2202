#!/bin/sh
# @desc Config variables (common version -- stored in repository)
# @changed 2022.01.03, 19:00

DIST_REPO="git@github.com:lilliputten/2201-march-nextjs-temp-splash.git"
DIST_BRANCH="publish"
SRC_TAG_PREFIX="v." # "v" for default "v.X.Y.Z"

PUBLISH_FOLDER="$DIST_BRANCH"

# TODO: To use generic `init-crossplatform-command-names.sh`
FINDCMD="find"
SORTCMD="sort"
GREPCMD="grep"
# Is it Windows?
IS_WINDOWS=`echo "${OS}" | grep -i windows`
if [ "$IS_WINDOWS" ]; then
    # Don't use windows' own native commands
    FINDCMD="find_"
    SORTCMD="sort_"
    GREPCMD="grep_"
fi
