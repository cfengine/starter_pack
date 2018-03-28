#!/usr/bin/env bash

vagrant destroy -f basebox
rm -f base.box

set -e
set -x

vagrant box update basebox
vagrant up basebox
vagrant package basebox --output base.box
vagrant destroy -f basebox
vagrant box remove -f basebox || echo "Warning: Couldn't remove previous basebox"
vagrant box add basebox base.box
rm -f base.box || echo "Warning: Couldn't delete base.box"
