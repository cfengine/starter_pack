#!/usr/bin/env bash

# Install a bunch of packages noninteractively:
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade
apt-get install -y emacs24 git nano
apt-get install -y ntp
apt-get install -y gdb automake autoconf libtool
apt-get install -y python-pip python3-pip
apt-get install -y libssl-dev libpcre3 libpcre3-dev
apt-get install -y bison libbison-dev libacl1 libacl1-dev libpq-dev
apt-get install -y lmdb-utils liblmdb-dev libpam0g-dev flex
apt-get install -y libtokyocabinet-dev
apt-get install -y unzip
apt-get install -y cargo

# Nova deps:
echo 'deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main' >> /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
apt-get update

function init_bashrc {
    touch /home/vagrant/.bashrc
    touch /home/vagrant/.bash_profile
    touch /root/.bashrc
    touch /root/.bash_profile
}

function add_line_if_not_found {
    grep -q -F "$1" $2 || echo "$1" >> $2
}

function add_to_path {
    init_bashrc
    line="export PATH=$PATH:$1"
    add_line_if_not_found "$line" "/home/vagrant/.bashrc"
    add_line_if_not_found "$line" "/home/vagrant/.bash_profile"
    add_line_if_not_found "$line" "/root/.bashrc"
    add_line_if_not_found "$line" "/root/.bash_profile"
}

apt-get install -y postgresql-10 postgresql-contrib-10 # libpq-dev pgadmin3
add_to_path "/usr/lib/postgresql/10/bin"
apt-get install -y python-psycopg2
apt-get install -y libpgtypes3 libecpg-dev libhiredis-dev libldap2-dev
apt-get install -y python-software-properties
add-apt-repository -y ppa:ondrej/php
apt-get update
apt-get install -y --force-yes php7.0-dev

# mingw cross compile deps:
apt-get install -y dpkg-dev debhelper g++ libncurses5 pkg-config build-essential libpam0g-dev mingw-w64

# Remove unneeded packages and cache:
apt-get -y autoremove
apt-get -y clean

mkdir /root/redis && cd /root/redis || exit 1
wget http://download.redis.io/releases/redis-3.2.11.tar.gz
tar xzf redis-3.2.11.tar.gz
cd redis-3.2.11 || exit 1
make
make install

# The basebox is only for downloading and installing time consuming deps
# Do all other configuration in the other bootstrap.sh script

history -c
