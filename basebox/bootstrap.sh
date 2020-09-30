#!/usr/bin/env bash

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

# Install a bunch of packages noninteractively:
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade
apt-get install -y emacs git nano
apt-get install -y ntp
apt-get install -y gdb automake autoconf libtool
apt-get install -y python-pip python3-pip
apt-get install -y libssl-dev libpcre3 libpcre3-dev
apt-get install -y bison libbison-dev libacl1 libacl1-dev libpq-dev
apt-get install -y lmdb-utils liblmdb-dev libpam0g-dev flex
apt-get install -y libtokyocabinet-dev
apt-get install -y unzip
apt-get install -y cargo
apt-get install -y nodejs npm jq
npm install --global json5

# Nova deps:
echo 'deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main' >> /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
apt-get update

apt-get install -y postgresql-11 postgresql-contrib-11 # libpq-dev pgadmin3
add_to_path "/usr/lib/postgresql/11/bin"
apt-get install -y python-psycopg2
apt-get install -y libpgtypes3 libecpg-dev libldap2-dev
apt-get install -y python-software-properties
add-apt-repository -y ppa:ondrej/php
apt-get update
apt-get install -y --force-yes php7.3-dev

source /etc/os-release
echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key | sudo apt-key add -
apt-get update
apt-get -y install podman buildah

# mingw cross compile deps:
apt-get install -y dpkg-dev debhelper g++ libncurses5 pkg-config build-essential libpam0g-dev mingw-w64

# Remove unneeded packages and cache:
apt-get -y autoremove
apt-get -y clean

mkdir -p /home/vagrant/.ssh
cp /vagrant/keys/insecure.pub /home/vagrant/.ssh/id_rsa.pub
cp /vagrant/keys/insecure /home/vagrant/.ssh/id_rsa
chown vagrant:vagrant /home/vagrant/.ssh/id_rsa
chown vagrant:vagrant /home/vagrant/.ssh/id_rsa.pub
chmod 600 /home/vagrant/.ssh/id_rsa
chmod 600 /home/vagrant/.ssh/id_rsa.pub

history -c
