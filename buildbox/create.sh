#!/usr/bin/env bash

vagrant destroy -f buildbox
vagrant box update buildbox
vagrant up buildbox
rm -f build.box
vagrant package buildbox --output build.box
vagrant destroy -f buildbox
vagrant box remove -f buildbox
vagrant box add buildbox build.box
rm -f build.box
