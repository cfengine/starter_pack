#!/usr/bin/env bash

set -e

checkout()
{
    echo $2 $1
    cd ./$2
    git fetch --all --tags
    git checkout $1
    git rebase upstream/$1
    cd ..
    echo
}

checkout 3.12.x core
checkout 3.12.x masterfiles
checkout 3.12.x enterprise
checkout 3.12.x nova
checkout 3.12.x mission-portal
checkout 3.12.x ldap-api
checkout 3.12.x buildscripts
checkout 3.12 documentation
checkout master documentation-generator
checkout master infra
