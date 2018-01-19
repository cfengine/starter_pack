#!/usr/bin/env bash

set -e
set -x

vagrant destroy -f buildslavebox
vagrant box update buildslavebox
vagrant up buildslavebox
rm -f buildslave.box
vagrant package buildslavebox --output buildslave.box
vagrant destroy -f buildslavebox
vagrant box remove -f buildslavebox
vagrant box add buildslavebox buildslave.box
rm -f buildslave.box
