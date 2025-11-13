# CFEngine starter pack

CFEngine enterprise can be pretty hard/tedious to build, because of many repos and dependencies.
This is an attempt to make it easier for new developers.
It is by no means finished, please add GitHub Issues and Pull Requests :)

## Installing vagrant and virtualbox

It is recommended, but not required, to run builds and tests inside VMs managed by vagrant.

Install virtualbox:
https://www.virtualbox.org/

Install vagrant:
https://www.vagrantup.com/docs/installation/

Install guest additions plugin:

```
vagrant plugin install vagrant-vbguest
```

It is also possible to use libvirt (KVM) instead of VirtualBox. Apart from the
working `qemu-kvm` setup and `libvirt`, the `vagrant-libvirt` plugin has to be
installed too. It may either be provided as a package in your distribution or it
can be installed by vagrant itself:

```
vagrant plugin install vagrant-libvirt
```

Please see the [libvirt notes](#libvirt-notes) section for some more details and
suggestions.

## Recommended setup

### Folder structure

Have all your Northern.tech projects in
`/northern.tech`. Or export `NTECH_ROOT` with the path to your base
folder.

For example:

```
export NTECH_ROOT="$HOME/northern.tech"
```

CFEngine projects in `$NTECH_ROOT/cfengine` (similar for zener, and so on.)
The reason to place it at root is so it can have the same absolute path on all VMs, using a mounted shared folder.
It is not a strict requirement, it's just easier.
If you use another path, you will have to update Vagrantfile and bash scripts.

Something like this does the job:

```
sudo mkdir -p /northern.tech/cfengine
export NTECH_ROOT=/northern.tech
cd $NTECH_ROOT/cfengine
git clone git@github.com:cfengine/starter_pack.git
```

If your local username doesn't match your github username then provide it to clone.sh

```
bash ./starter_pack/repos/clone.sh my_github_username
cd starter_pack
```

If they match, just use:

```
bash ./starter_pack/repos/clone.sh
cd starter_pack
```

**Note:** The `clone.sh` script clones all CFEngine repos into the current directory

### SSH keys

```
bash scripts/keygen.sh
```

Will generate `./keys/insecure[.pub]`.
This will be installed to `~/.ssh/id_rsa[.pub]` on all vagrant machines.
`./keys/insecure.pub` is added to build user's `authorized_keys` so build-remote can work.

The `Vagrantfile` also has code to copy your SSH key from your home directory, to `authorized_keys` in the VMs, so you can use regular `ssh` commands (instead of `vagrant ssh`).

### Custom init script

If you'd like to make custom changes to the VMs, such as fixing your `PATH` variable, or installing your own dotfiles, you can put code in the file `./scripts/custom_vm_init.sh`.
This file is ignored by git, so won't be committed, it will be custom to you.
As an example, here is what I (Ole) have in my `./scripts/custom_vm_init.sh`:

```
#!/usr/bin/env bash
curl -L -s https://raw.githubusercontent.com/olehermanse/dotfiles/master/install.sh | bash
```

## Getting started with the dev machine

The development machine has all development libraries already installed.
It is ready to run autogen, make etc.
It will **NOT** work with `build-remote`.
(See the sections on the buildslave machine below.)

### Creating a base box for development

The vagrant VMs use a custom base box where some dependencies are installed.
To create this box locally, run:

```
bash ./basebox/create.sh
```

(vagrant required).
This will run commands from `basebox/bootstrap.sh` on an Ubuntu VM.
If you're not using vagrant, you can run/adapt that script on a build/development machine of your choice.

If you get the following error:

```
/home/larsewi/.vagrant.d/gems/3.3.8/gems/vagrant-vbguest-0.32.0/lib/vagrant-vbguest/hosts/virtualbox.rb:84:in `block in guess_local_iso': undefined method `exists?' for class File (NoMethodError)

            path && File.exists?(path)
                        ^^^^^^^^
Did you mean?  exist?
```

Then, the reason is a bug in `vagrant-vbguest` plugin. This is an archived repository.
So it will not be fixed any time soon. You'd better just fix it yourself. E.g.:

```
sed -i 's/File.exists/File.exist/g' ~/.vagrant.d/gems/3.3.8/gems/vagrant-vbguest-0.32.0/lib/vagrant-vbguest/hosts/virtualbox.rb
```

### Starting the development machine

```
vagrant up dev
```

If you ever need a clean dev machine, log out and:

```
vagrant destroy dev
```

followed by:

```
vagrant up dev
```

This is great, because you don't have to be careful not to mess up your dev machine.
You can always get a new one within a minute.

### Compiling CFEngine Community in the development machine

Login to dev machine:

```
vagrant ssh dev
```

Configure and compile CFEngine Core:

```
cd /northern.tech/cfengine/core
./autogen.sh --enable-debug
make -j2
```

Configure the Masterfiles Policy Framework:

```
cd ../masterfiles
./autogen.sh
```

### Installing CFEngine Community on a test machine

#### Hub

Bring up and login to the hub machine:

```
vagrant up hub
vagrant ssh hub
```

Configure, compile and install CFEngine Core:

```
cd /northern.tech/cfengine/core
./configure && make && sudo make -j2 install
```

Configure and install the Masterfiles Policy Framework:

```
cd ../masterfiles
./configure && make && sudo make -j2 install
```

Generate keys and bootstrap to self (as root):

```
sudo /var/cfengine/bin/cf-key
sudo /var/cfengine/bin/cf-agent --bootstrap 192.168.56.90
```

**Note:** You could use `localhost` as the IP, but this would prevent other hosts from bootstrapping to the hub.

#### Client

Bring up and login to the hub machine:

```
vagrant up client
vagrant ssh client
```

Configure, compile and install CFEngine Core:

```
cd /northern.tech/cfengine/core
./configure && make && sudo make -j2 install
```

Generate keys and bootstrap to hub:

```
sudo /var/cfengine/bin/cf-key
sudo /var/cfengine/bin/cf-agent --bootstrap 192.168.56.90
```

## build-remote on buildslave

The `buildslave` machine is set up specifically for the `build-remote` script.
This script checks that certain dependencies are installed, while others are not installed, to avoid conflicting dependencies.
Running `build-remote` from `dev` VM to `buildslave` VM is the easiest.

If you haven't already, create the buildslave base box:

```
bash ./buildslave/create.sh
```

This VM has some extra dependencies for performing buildslave tasks.
You can now use build-remote from dev machine to build on buildslave.

Bring up the build machine:

```
vagrant up buildslave
```

Bring up and login to the dev machine:

```
vagrant up dev
vagrant ssh dev
```

Login to buildmachine from dev machine:

```
ssh build@buildslave
```

Answer yes to verify the authenticity of the host:

```
The authenticity of host 'buildslave (192.168.56.100)' can't be established.
ECDSA key fingerprint is SHA256:VoU/qb7Y7Pt1HYBw7ze1DXHF3E99hQvhBjoUjme9+3c.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'buildslave,192.168.56.100' (ECDSA) to the list of known hosts.
```

Type logout or simply press `CTRL + D` to return to the dev machine:

```
logout
```

**Didn't work?** Check out [Troubleshooting](#troubleshooting)

From the dev machine, execute the build-remote script:

```
bash /northern.tech/buildscripts/build-remote --no-tests --source /northern.tech/ --role hub --verbose build@buildslave
```

Your build files will appear here:

```
~/workdir-nova-master-build@buildslave/build/output/nova-master-localbuild/current/--/
```

You can i.e. copy the deb package to the `/vagrant` directory:

```
cp workdir-nova-master-build@buildslave/build/output/nova-master-localbuild/current/--/cfengine-nova-hub_*.deb /vagrant/
```

Login to you hub machine `CTRL + D` followed by:

```
vagrant ssh hub
```

Make sure to remove PostgreSQL:

```
sudo apt purge postgres*
```

Install with:

```
mv /vagrant/cfengine-nova-hub_*.deb ~/
sudo dpkg -i cfengine-nova_3.27.0a.ef005c5af~unknown.ubuntu22_amd64.deb
```

### Example: mingw cross compile for windows using build-remote

```
bash /northern.tech/cfengine/buildscripts/build-remote -c x64-mingw --source /northern.tech/cfengine --verbose build@buildslave
```

This currently works for building dependencies as well as our binaries, but not packaging.
The `wix.exe` dependency is not installed on buildslave, and adding it is not trivial.

If you need packages to test your code, a workaround is to get jenkins to build a package.
You can then install the package once, and as you make changes, upload the locally compiled `.exe` files via `scp` or similar.

## Building CFEngine Enterprise locally

### Compiling core, enterprise and nova on the dev machine

Bring up and login to the dev machine:

```
vagrant up dev
vagrant ssh dev
```

Using `cf-builder.py`:

```
cd /northern.tech/cfengine/starter_pack
python3 cf-builder.py --autogen --make --core --masterfiles --enterprise --nova
```

By running:

```
python3 cf-builder.py --build-all --dry-run
```

the individual steps will be outputted:

```
These commands would run if you didn't specify --dry-run:
cd /northern.tech/cfengine && cd core && ./autogen.sh --enable-debug
cd /northern.tech/cfengine && cd core && make -j2
cd /northern.tech/cfengine && cd enterprise && ./autogen.sh --enable-debug
cd /northern.tech/cfengine && cd enterprise && make -j2
cd /northern.tech/cfengine && cd nova && ./autogen.sh --enable-debug --with-postgresql-hub=/usr
cd /northern.tech/cfengine && cd nova && make -j2
```

(You can run the steps without using `cf-builder.py`, simplify the `cd` commands if you'd like)

### WIP! Installing CFEngine Enterprise on hub machine

In general, don't install on your dev machine, and don't run sudo commands on the dev machine.
Everything you're doing there should work without sudo.
Use the `hub` and `client` machines to install and bootstrap.

After compiling on `dev` machine, use `cf-builder.py` to install on `hub`.

Bring up and login to the hub machine:

```
vagrant up hub
vagrant ssh hub
```

Install CFEngine Enterprise (as root):

```
cd /northern.tech/cfengine/starter_pack
sudo python3 cf-builder.py --install --all-repos
```

Generate keys, initialize the database and bootstrap to self (as root):

```
sudo /var/cfengine/bin/cf-key
sudo bash scripts/initdb.sh
sudo /var/cfengine/bin/cf-agent --bootstrap 192.168.56.90
```

### WIP! Running no-install reporting test

## docs.cfengine.com

The documentation is built with Jekyll and some custom tooling. Some very
specific tool versions are supported.

- [cfengine/documentation](https://github.com/cfengine/documentation)
- [cfengine/documentation-generator](https://github.com/cfengine/documentation-generator)

### Bring up build host

```
vagrant up docbuildslave
```

During provisioning it runs `_scripts/provisioning-install-build-tool-chain.sh`

To perform a build log into docbuildslave and run `starter_pack/build-docs.sh`
from the documentation-generator repository.

```
vagrant ssh docbuildslave
vagrant@docbuildslave ~ $ bash /northern.tech/cfengine/documentation-generator/_scripts/starter_pack-build-docs.sh
```

Browse the site in `$NTECH_ROOT/cfengine/documentation-generator/_site/index.html`

#### How Nick last build successfully

These are some raw notes about how I last used this successfully. I iterated until I got a successful run of jekyll, site preview didn't quite work, but it helped me iterate on fixing up links which can be difficult if the auto linking doesn't work.

```
rm -rf /northern.tech/cfengine/documentation
rsync -avz ~/CFEngine/documentation /northern.tech/cfengine/
rm -rf /northern.tech/cfengine/documentation-generator
rsync -avz ~/CFEngine/documentation-generator /northern.tech/cfengine/

cd /northern.tech/cfengine/core
git checkout master
git pull --rebase upstream master

cd /northern.tech/cfengine/mission-portal
git checkout master
git pull --rebase upstream master

cd /northern.tech/cfengine/nova
git checkout master
git pull --rebase upstream master

cd /northern.tech/cfengine/masterfiles
git checkout master
git pull --rebase upstream master

cd /northern.tech/cfengine/enterprise
git checkout master
git pull --rebase upstream master

cd /northern.tech/cfengine/nova
git checkout master
git pull --rebase upstream master

cd ~/CFEngine/starter_pack
vagrant rsync docbuildslave
vagrant ssh docbuildslave -c "bash /northern.tech/cfengine/documentation-generator/_scripts/starter_pack-build-docs.sh"

vagrant ssh-config docbuildslave > /tmp/docbuildslave.ssh-config
scp -rF /tmp/docbuildslave.ssh-config docbuildslave:/northern.tech/cfengine/documentation-generator/_site ./
```

### Installing a pre-built hub package

The `hub` VM comes with dependencies already installed to make it easy to build and install CFEngine Enterprise hub locally.
If you would rather install a pre-built hub package, remove PostgreSQL:

```
apt purge postgresql*
wget http://buildcache.cfengine.com/packages/testing-pr/jenkins-pr-pipeline-9281/PACKAGES_HUB_x86_64_linux_ubuntu_20/cfengine-nova-hub_3.22.0a.8c38b8b08~25630.ubuntu20_amd64.deb
sudo dpkg -i cfengine-nova-hub_*.deb
sudo /var/cfengine/bin/cf-agent -B 192.168.56.90
```

(This is just an example using the URL from a PR build, replace the 2nd line with the hub package you want to test, or use cf-remote, etc.)

You should be able to open MP in your browser with the IP afterwards:

https://192.168.56.90/

### Notes and TODOs

The .git subdirectories get deleted during `_run_jekyll.sh` but I don't know
why. Perhaps something to do with jenkins. So you will want to keep a separate
repo and sync your changes to it.

```
rsync -avz $NTECH_ROOT/cfengine/documentation $HOME/CFEngine/documentation/
```

## libvirt notes

### Building baseboxes

There is a step in the `create.sh` scripts for building baseboxes where they try
to package the box (e.g. `vagrant package basebox --output base.box`). This may
fail due to the VM image file not being readable for the current user. However,
_vagrant_ even prints out the command to fix it (change the permissions) so just
run the suggested command. Unfortunately, the `create.sh` script stops on this
so the particular step has to be run again and then all the follow-up steps have
to be run. It would be nice if the permissions could be fixed in advance, but
there seems to be no easy way to get the image path for a given vagrant machine.

### Synced folders

vagrant-libvirt doesn't support the mechanisms for sharing folders between VMs
and the host system. So it either uses _rsync_ to sync the folders (that's why
we have some extra rsync options in the `Vagrantfile`) or sets up NFS to share
the folders. However, it quite often fails to set NFS up properly, so it may be
necessary to enforce rsync syncing. This can be done by adding `type: "rsync"` to
the `synced_folder` lines. So something like this:

```
-    config.vm.synced_folder ".", "/vagrant",
+    config.vm.synced_folder ".", "/vagrant", type: "rsync",
```

## Troubleshooting

### ssh: connect to host 192.168.56.100 port 22: Protocol not available

If you get the following error when trying to ssh into the buildslave from the dev machine:

```
ssh: connect to host 192.168.56.100 port 22: Protocol not available
```

Then I experienced the same issue. Not sure if it was an ARP cache bug or a lingering ghost VM.
Nevertheless, when I tried to connect, I saw that the ARP cache was updated with a different MAC address then that of the buildslave.
However, by doing the reverse connection. E.g. (run this command from your host machine):

```
vagrant ssh buildslave -c "ping -c1 192.168.56.10"
```

I was able to repopulate the ARP cache with the correct MAC address.
