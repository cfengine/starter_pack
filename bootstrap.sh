#!/usr/bin/env sh

# Remove welcome message:
touch /root/.hushlogin
touch /home/vagrant/.hushlogin

# Hostname entry for buildmachine:
grep -q -F 'buildmachine' /etc/hosts || echo '192.168.100.100 buildmachine' >> /etc/hosts


promptv='export PS1="\t \h:\u \W $ "'
# Replace prompt
grep -q -F "\'$promptv\'" /home/vagrant/.bashrc       || echo "\'$promptv\'" >> /home/vagrant/.bashrc
grep -q -F "\'$promptv\'" /home/vagrant/.bash_profile || echo "\'$promptv\'" >> /home/vagrant/.bash_profile
grep -q -F "\'$promptv\'" /root/.bashrc               || echo "\'$promptv\'" >> /root/.bashrc
grep -q -F "\'$promptv\'" /root/.bash_profile         || echo "\'$promptv\'" >> /root/.bash_profile
