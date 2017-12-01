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

# Replace prompt
grep -q -F 'export PS1="\u@\h \W $ "' /home/vagrant/.bashrc       || echo 'export PS1="\u@\h \W $ "' >> /home/vagrant/.bashrc
grep -q -F 'export PS1="\u@\h \W $ "' /home/vagrant/.bash_profile || echo 'export PS1="\u@\h \W $ "' >> /home/vagrant/.bash_profile
grep -q -F 'export PS1="\u@\h \W $ "' /root/.bashrc               || echo 'export PS1="\u@\h \W $ "' >> /root/.bashrc
grep -q -F 'export PS1="\u@\h \W $ "' /root/.bash_profile         || echo 'export PS1="\u@\h \W $ "' >> /root/.bash_profile
