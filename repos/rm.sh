#!/usr/bin/env sh

read -p "Delete CFEngine repos in current directory (y/n)? " choice
case "$choice" in 
  y|Y ) echo "Proceeding to delete all CFEngine repos in current directory";;
  n|N ) exit 1;;
  * ) exit 1;;
esac

cfengine_rm(){
    if [ -d "$1" ]; then
        echo "Deleting $1..."
        rm -rf $1
    else
        echo "$1 doesn't exist"
    fi
}

cfengine_rm core
cfengine_rm enterprise
cfengine_rm nova
cfengine_rm mission-portal
cfengine_rm buildscripts
cfengine_rm documentation
cfengine_rm documentation-generator
