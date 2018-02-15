#!/usr/bin/env bash
yum update -y
yum install -y epel-release
yum install -y centos-release-scl
yum install -y lmdb-devel
yum install -y autoconf
yum install -y automake
yum install -y openssl-devel
yum install -y pam-devel
yum install -y byacc
yum install -y flex
yum install -y flex-devel
