#!/usr/bin/env bash

set -e
set -x

vagrant destroy -f basebox
vagrant box update basebox
vagrant up basebox
rm -f base.box
vagrant package basebox --output base.box
vagrant destroy -f basebox
vagrant box remove -f basebox
vagrant box add basebox base.box
rm -f base.box
