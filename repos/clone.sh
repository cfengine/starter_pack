#!/usr/bin/env sh

user=${1:-$(whoami)}

cloner(){
    if [ -d "$2" ]; then
        echo "$2 already exists"
    else
        git clone --recursive --origin upstream git@github.com:$1/$2.git && \
        cd $2 && \
        git remote add origin git@github.com:${user}/$2.git && \
        git fetch --all --tags && \
        cd ..
    fi
}

cfengine_clone(){
    cloner cfengine $1
}

mender_clone(){
    cloner mendersoftware $1
}

cfengine_clone core
cfengine_clone masterfiles
cfengine_clone enterprise
cfengine_clone nova
cfengine_clone mission-portal
cfengine_clone buildscripts
cfengine_clone documentation
cfengine_clone system-testing
mender_clone infra
