#!/usr/bin/env sh

# Remove welcome message:
touch /root/.hushlogin
touch /home/vagrant/.hushlogin
chown vagrant:vagrant /home/vagrant/.hushlogin

# Manipulate hostnames to make sure localhost and buildslave names are correct:
touch /etc/hosts

# Remove entries created by vagrant:
# sed -i '/buildslave/d' /etc/hosts
# sed -i "/$(hostname)/d" /etc/hosts

# Add buildslave entry on all machines:
echo "" >> /etc/hosts
grep 'buildslave' /etc/hosts || echo '192.168.56.100 buildslave' >> /etc/hosts
echo "" >> /etc/hosts

touch /root/.bashrc
touch /root/.bash_profile
touch /home/vagrant/.bashrc
touch /home/vagrant/.bash_profile
chown vagrant:vagrant /home/vagrant/.bashrc
chown vagrant:vagrant /home/vagrant/.bash_profile

# Replace prompt
grep -q -F 'export PS1="\u@\h \W $ "' /home/vagrant/.bashrc       || echo 'export PS1="\u@\h \W $ "' >> /home/vagrant/.bashrc
grep -q -F 'export PS1="\u@\h \W $ "' /home/vagrant/.bash_profile || echo 'export PS1="\u@\h \W $ "' >> /home/vagrant/.bash_profile
grep -q -F 'export PS1="\u@\h \W $ "' /root/.bashrc               || echo 'export PS1="\u@\h \W $ "' >> /root/.bashrc
grep -q -F 'export PS1="\u@\h \W $ "' /root/.bash_profile         || echo 'export PS1="\u@\h \W $ "' >> /root/.bash_profile

# Optional custom script (for adding user config / dotfiles for example):
INIT_SCRIPT="/vagrant/scripts/custom_vm_init.sh"

if [ -f "$INIT_SCRIPT" ]; then
    bash "$INIT_SCRIPT"
    su -c "bash $INIT_SCRIPT" vagrant
fi
