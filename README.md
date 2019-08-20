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
$ vagrant plugin install vagrant-vbguest
```

It is also possible to use libvirt (KVM) instead of VirtualBox. Apart from the
working `qemu-kvm` setup and `libvirt`, the `vagrant-libvirt` plugin has to be
installed too. It may either be provided as a package in your distribution or it
can be installed by vagrant itself:
```
$ vagrant plugin install vagrant-libvirt
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
export NTECH_ROOT="$HOME/Northern.Tech"
```

CFEngine projects in `$NTECH_ROOT/cfengine` (similar for zener, and so on.)
The reason to place it at root is so it can have the same absolute path on all VMs, using a mounted shared folder.
It is not a strict requirement, it's just easier.
If you use another path, you will have to update Vagrantfile and bash scripts.

Something like this does the job:
```
$ sudo mkdir -p /northern.tech/cfengine
$ export NTECH_ROOT=/northern.tech
$ cd $NTECH_ROOT/cfengine
$ git clone git@github.com:cfengine/starter_pack.git
$ bash ./starter_pack/repos/clone.sh
$ cd starter_pack
```

**Note:** The `clone.sh` script clones all CFEngine repos into the current directory

### SSH keys

```
bash scripts/keygen.sh
```

Will generate `./keys/insecure[.pub]`.
This will be installed to `~/.ssh/id_rsa[.pub]` on all vagrant machines.
`./keys/insecure.pub` is added to build user's `authorized_keys` so build-remote can work.

## Getting started with the dev machine
The development machine has all development libraries already installed.
It is ready to run autogen, make etc.
It will **NOT** work with `build-remote`.
(See the sections on the buildslave machine below.)

### Creating a base box for development
The vagrant VMs use a custom base box where some dependencies are installed.
To create this box locally, run:
```
$ bash ./basebox/create.sh
```
(vagrant required).
This will run commands from `basebox/bootstrap.sh` on an Ubuntu VM.
If you're not using vagrant, you can run/adapt that script on a build/development machine of your choice.

### Starting the development machine
```
$ vagrant up dev
```

If you ever need a clean dev machine, log out and:
```
$ vagrant destroy dev
$ vagrant up dev
```
This is great, because you don't have to be careful not to mess up your dev machine.
You can always get a new one within a minute.

### Compiling CFEngine Community in the development machine
```
$ vagrant ssh dev
$ cd /northern.tech/cfengine/core
$ ./autogen.sh --enable-debug
$ make -j2
$ cd ../masterfiles
$ ./autogen.sh --enable-debug
```

### Installing CFEngine Community on a test machine

#### Hub
```
$ vagrant up hub
$ vagrant ssh hub
$ cd /northern.tech/cfengine/core
$ ./configure && make && sudo make -j2 install
$ cd ../masterfiles
$ ./configure && make && sudo make -j2 install
$ sudo su -
# /var/cfengine/bin/cf-key
# /var/cfengine/bin/cf-agent --bootstrap 192.168.80.90
```

#### Client
```
$ vagrant up client
$ vagrant ssh client
$ cd /northern.tech/cfengine/core
$ ./configure && make && sudo make -j2 install
$ sudo su -
# /var/cfengine/bin/cf-key
# /var/cfengine/bin/cf-agent --bootstrap 192.168.80.90
```

## build-remote on buildslave

The `buildslave` machine is set up specifically for the `build-remote` script.
This script checks that certain dependencies are installed, while others are not installed, to avoid conflicting dependencies.
Running `build-remote` from `dev` VM to `buildslave` VM is the easiest.

### Creating a buildslave base box
```
$ bash ./buildslave/create.sh
```

### Starting the build slave
```
$ vagrant up buildslave
```

### Testing ssh for build-remote
```
$ vagrant ssh dev
$ ssh build@buildslave
$ exit
```
(Should not ask for password)

### Running build-remote
```
$ cd /northern.tech/cfengine/buildscripts
$ bash build-remote --verbose --source /northern.tech/cfengine/ build@buildslave
```
**Note:** The `build-remote` script will put output in `/northern.tech/cfengine/output`

## Building CFEngine Enterprise locally

### Compiling core, enterprise and nova on the dev machine

Using `cf-builder.py`:
```
$ vagrant up dev
$ vagrant ssh dev
$ cd /northern.tech/cfengine/starter_pack
$ python3 cf-builder.py --autogen --make --core --masterfiles --enterprise --nova
```

The individual steps:
```
$ python3 cf-builder.py --build-all --dry-run

These commands would run if you didn't specify --dry-run:
cd /northern.tech/cfengine && cd core && ./autogen.sh --enable-debug
cd /northern.tech/cfengine && cd core && make -j2
cd /northern.tech/cfengine && cd enterprise && ./autogen.sh --enable-debug
cd /northern.tech/cfengine && cd enterprise && make -j2
cd /northern.tech/cfengine && cd nova && ./autogen.sh --enable-debug --with-postgresql-hub=/usr
cd /northern.tech/cfengine && cd nova && make -j2
```
(You can run the steps without using `cf-builder.py`, simplify the `cd` commands if you'd like)

### WIP! Installing CFEngine on hub machine

In general, don't install on your dev machine, and don't run sudo commands on the dev machine.
Everything you're doing there should work without sudo.
Use the `hub` and `client` machines to install and bootstrap.

After compiling on `dev` machine, use `cf-builder.py` to install on `hub`:
```
$ vagrant up hub
$ vagrant ssh hub
$ sudo su
$ cd /northern.tech/cfengine/starter_pack
$ python3 cf-builder.py --install --all-repos
$ /var/cfengine/bin/cf-key
$ bash scripts/initdb.sh
$ /var/cfengine/bin/cf-agent --bootstrap 192.168.80.90
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
*vagrant* even prints out the command to fix it (change the permissions) so just
run the suggested command. Unfortunately, the `create.sh` script stops on this
so the particular step has to be run again and then all the follow-up steps have
to be run. It would be nice if the permissions could be fixed in advance, but
there seems to be no easy way to get the image path for a given vagrant machine.

### Synced folders

vagrant-libvirt doesn't support the mechanisms for sharing folders between VMs
and the host system. So it either uses *rsync* to sync the folders (that's why
we have some extra rsync options in the `Vagrantfile`) or sets up NFS to share
the folders. However, it quite often fails to set NFS up properly, so it may be
necesary to enforce rsync syncing. This can be done by adding `type: "rsync"` to
the `synced_folder` lines. So something like this:
```
-    config.vm.synced_folder  ".", "/vagrant",
+    config.vm.synced_folder  ".", "/vagrant", type: "rsync",
```
