#!/usr/bin/env sh

cfengine_rebase(){
    if [ -d "$1" ]; then
        cd "$1" || exit 1;
        echo "$1:";
        git fetch upstream
        git rebase upstream/master
        cd - > /dev/null || exit 1;
    else
        echo "$1 doesn't exist!"
    fi
}

cfengine_rebase core
cfengine_rebase enterprise
cfengine_rebase nova
cfengine_rebase mission-portal
cfengine_rebase buildscripts
cfengine_rebase documentation
cfengine_rebase documentation-generator
