#!/usr/bin/env bash

set -e
set -x

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

# /northern.tech/cfengine/mission-portal/scripts/bootstrap.sh
umask 0022

# install the custom PHP repository
if grep -iq ubuntu /etc/os-release; then
    add-apt-repository -y ppa:ondrej/php
else
    if [ ! -f "/etc/apt/sources.list.d/sury-php.list" ]; then
        apt-get update
        apt-get install -y lsb-release ca-certificates apt-transport-https software-properties-common gnupg2
        echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/sury-php.list
        wget -qO - https://packages.sury.org/php/apt.gpg | sudo apt-key add -
    fi
fi

# install nodejs and npm
if [ ! -f "£/etc/apt/sources.list.d/nodesource.list" ]; then
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
    apt-get install -y nodejs
fi

# install the custom PostgreSQL repository
if [ ! -f "/etc/apt/sources.list.d/pgdg.list" ]; then
    apt-get update
    apt-get install -y lsb-release ca-certificates apt-transport-https software-properties-common gnupg2
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
    wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
fi

# install the build and runtime dependencies
apt-get update
apt-get install -y \
    acl \
    automake \
    build-essential \
    bison \
    flex \
    git \
    libacl1-dev \
    libapreq2-dev \
    libaprutil1-dev \
    libcurl4-openssl-dev \
    libldap2-dev \
    liblmdb-dev \
    libtool \
    libdb-dev \
    libpam0g-dev \
    libpcre3-dev \
    libpq-dev \
    libssl-dev \
    libxml2-dev \
    lsb-release \
    pkg-config \
    postgresql-13 \
    unzip \
    zlib1g-dev

mkdir -p /home/vagrant/.ssh
cp /vagrant/keys/insecure.pub /home/vagrant/.ssh/id_rsa.pub
cp /vagrant/keys/insecure /home/vagrant/.ssh/id_rsa
chown vagrant:vagrant /home/vagrant/.ssh/id_rsa
chown vagrant:vagrant /home/vagrant/.ssh/id_rsa.pub
chmod 600 /home/vagrant/.ssh/id_rsa
chmod 600 /home/vagrant/.ssh/id_rsa.pub

history -c
