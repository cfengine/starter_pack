#!/usr/bin/env sh

# Remove welcome message:
touch /root/.hushlogin
touch /home/vagrant/.hushlogin

# Hostname entry for buildmachine:
touch /etc/hosts
grep -q -F 'buildmachine' /etc/hosts || echo '192.168.100.100 buildmachine' >> /etc/hosts

touch /home/vagrant/.bashrc
touch /home/vagrant/.bash_profile
touch /root/.bashrc
touch /root/.bash_profile

ssh-keygen -t rsa -f /home/vagrant/.ssh/id_rsa -N ""
chown vagrant:vagrant /home/vagrant/.ssh/id_rsa
chmod 600 /home/vagrant/.ssh/id_rsa

echo '' >> /etc/ssh/ssh_config
echo 'Host 127.0.0.1 buildmachine' >> /etc/ssh/ssh_config
echo '   StrictHostKeyChecking no' >> /etc/ssh/ssh_config
echo '   UserKnownHostsFile=/dev/null' >> /etc/ssh/ssh_config

useradd -m -s /bin/bash -U build
mkdir /home/build/.ssh
touch /home/build/.hushlogin

cp /home/vagrant/.ssh/authorized_keys /home/build/.ssh/authorized_keys
touch /vagrant/id_rsa.pub
cat /home/vagrant/.ssh/id_rsa.pub >> /home/build/.ssh/authorized_keys
cat /vagrant/id_rsa.pub >> /home/build/.ssh/authorized_keys

chown build:build /home/build/.ssh/authorized_keys
chmod 600 /home/build/.ssh/authorized_keys
echo ""                                           >> /etc/ssh/sshd_config
echo "passwordAuthentication no"                  >> /etc/ssh/sshd_config
echo "AuthorizedKeysFile %h/.ssh/authorized_keys" >> /etc/ssh/sshd_config

# Replace prompt
grep -q -F 'export PS1="\u@\h \W $ "' /home/vagrant/.bashrc       || echo 'export PS1="\u@\h \W $ "' >> /home/vagrant/.bashrc
grep -q -F 'export PS1="\u@\h \W $ "' /home/vagrant/.bash_profile || echo 'export PS1="\u@\h \W $ "' >> /home/vagrant/.bash_profile
grep -q -F 'export PS1="\u@\h \W $ "' /root/.bashrc               || echo 'export PS1="\u@\h \W $ "' >> /root/.bashrc
grep -q -F 'export PS1="\u@\h \W $ "' /root/.bash_profile         || echo 'export PS1="\u@\h \W $ "' >> /root/.bash_profile
