#!/usr/bin/env sh

cfengine_master(){
    if [ -d "$1" ]; then
        cd "$1" || exit 1;
        echo "$1:";
        git checkout master
        cd - > /dev/null || exit 1;
    else
        echo "$1 doesn't exist!"
    fi
}

cfengine_master core
cfengine_master masterfiles
cfengine_master enterprise
cfengine_master nova
cfengine_master mission-portal
cfengine_master buildscripts
cfengine_master documentation
cfengine_master documentation-generator