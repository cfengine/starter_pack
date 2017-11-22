#!/usr/bin/env sh

cfengine_clone(){
    if [ -d "$1" ]; then
        echo "$1 already exists"
    else
        git clone git@github.com:cfengine/$1.git
    fi
}

cfengine_clone core
cfengine_clone enterprise
cfengine_clone nova
cfengine_clone mission-portal
cfengine_clone buildscripts
cfengine_clone documentation
cfengine_clone documentation-generator
