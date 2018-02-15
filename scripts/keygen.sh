#!/usr/bin/env bash

set -e

mkdir keys
cd keys
ssh-keygen -t rsa -N "" -f insecure
