#!/usr/bin/env bash

# Install a bunch of packages noninteractively:
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y git
apt-get install -y gcc
apt-get install -y make
apt-get install -y libc-dev
apt-get install -y glibc-devel
apt-get install -y bison
apt-get install -y flex
apt-get install -y fakeroot

# Remove unneeded packages and cache:
apt-get -y autoremove
apt-get clean

history -c

apt-get -y autoremove

echo '' >> /etc/ssh/ssh_config
echo 'Host 127.0.0.1 buildmachine' >> /etc/ssh/ssh_config
echo '   StrictHostKeyChecking no' >> /etc/ssh/ssh_config
echo '   UserKnownHostsFile=/dev/null' >> /etc/ssh/ssh_config

ssh-keygen -t rsa -f /home/vagrant/.ssh/id_rsa -N ""
chown vagrant:vagrant /home/vagrant/.ssh/id_rsa
chmod 600 /home/vagrant/.ssh/id_rsa

useradd -m -s /bin/bash -U build
mkdir /home/build/.ssh
touch /home/build/.hushlogin

cp /home/vagrant/.ssh/authorized_keys /home/build/.ssh/authorized_keys
cat /home/vagrant/.ssh/id_rsa.pub >> /home/build/.ssh/authorized_keys

chown build:build /home/build/.ssh/authorized_keys
chmod 600 /home/build/.ssh/authorized_keys

echo ""                                           >> /etc/ssh/sshd_config
echo "passwordAuthentication no"                  >> /etc/ssh/sshd_config
echo "AuthorizedKeysFile %h/.ssh/authorized_keys" >> /etc/ssh/sshd_config
