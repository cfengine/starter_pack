#!/usr/bin/env bash

vagrant destroy -f custombox
vagrant box update custombox
vagrant up custombox
rm -f custom.box
vagrant package custombox --output custom.box
vagrant destroy -f custombox
vagrant box remove -f custombox
vagrant box add custombox custom.box
rm -f custom.box
