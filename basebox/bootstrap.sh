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

# Nova deps:
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | apt-key add -
apt-get install postgresql postgresql-contrib libpq-dev pgadmin3
apt-get install -y libpgtypes3 libecpg-dev libhiredis-dev libldap2-dev php5-dev

# mingw cross compile deps:
apt-get install -y dpkg-dev debhelper g++ libncurses5 pkg-config build-essential libpam0g-dev mingw-w64

# Remove unneeded packages and cache:
apt-get -y autoremove
apt-get clean

cp /vagrant/keys/insecure.pub /home/vagrant/.ssh/id_rsa.pub
cp /vagrant/keys/insecure /home/vagrant/.ssh/id_rsa
chown vagrant:vagrant /home/vagrant/.ssh/id_rsa
chown vagrant:vagrant /home/vagrant/.ssh/id_rsa.pub
chmod 600 /home/vagrant/.ssh/id_rsa
chmod 600 /home/vagrant/.ssh/id_rsa.pub

history -c
