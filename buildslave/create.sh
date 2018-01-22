#!/usr/bin/env bash

vagrant destroy -f buildslavebox
rm -f buildslave.box

set -e
set -x

vagrant box update buildslavebox
vagrant up buildslavebox
vagrant package buildslavebox --output buildslave.box
vagrant destroy -f buildslavebox
vagrant box remove -f buildslavebox
vagrant box add buildslavebox buildslave.box
rm -f buildslave.box
