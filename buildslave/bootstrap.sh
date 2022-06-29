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
apt-get install -y ntp
apt-get install -y pkg-config
apt-get install -y libpam0g-dev
apt-get install -y ntp
apt-get install -y dpkg-dev debhelper fakeroot
apt-get install -y libexpat1-dev

dpkg --add-architecture i386
apt-get update -qy
apt-get install -qy wine-development:i386 mingw-w64
apt-get install -qy bison flex ntp dpkg-dev python debhelper pkg-config default-jre-headless psmisc zip libmodule-load-conditional-perl python3-pip

# Remove unneeded packages and cache:
# for some reason libltdl7 must not be installed so let's make sure it really isn't
apt-get -y remove libltdl7
apt-get -y autoremove
apt-get clean

history -c

echo '' >> /etc/ssh/ssh_config
echo 'Host 127.0.0.1 buildmachine localhost' >> /etc/ssh/ssh_config
echo '   StrictHostKeyChecking no' >> /etc/ssh/ssh_config
echo '   UserKnownHostsFile=/dev/null' >> /etc/ssh/ssh_config

cp /vagrant/keys/insecure.pub /home/vagrant/.ssh/id_rsa.pub
cp /vagrant/keys/insecure /home/vagrant/.ssh/id_rsa
chown vagrant:vagrant /home/vagrant/.ssh/id_rsa
chown vagrant:vagrant /home/vagrant/.ssh/id_rsa.pub
chmod 600 /home/vagrant/.ssh/id_rsa
chmod 600 /home/vagrant/.ssh/id_rsa.pub

useradd -m -s /bin/bash -U build
mkdir /home/build/.ssh
touch /home/build/.hushlogin

echo "build ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
echo "" >> /etc/sudoers

cp /home/vagrant/.ssh/authorized_keys /home/build/.ssh/authorized_keys # Copy over vagrant ssh key
cat /vagrant/keys/insecure.pub >> /home/build/.ssh/authorized_keys     # Add insecure.pub

chown build:build /home/build/.ssh/authorized_keys
chmod 600 /home/build/.ssh/authorized_keys

echo ""                                           >> /etc/ssh/sshd_config
echo "passwordAuthentication no"                  >> /etc/ssh/sshd_config
echo "AuthorizedKeysFile %h/.ssh/authorized_keys" >> /etc/ssh/sshd_config
