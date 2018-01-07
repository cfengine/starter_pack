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

(If you know how to use libvirt/kvm or other virtualization software, feel free to use that).

## Recommended setup

### Folder structure

Have all your Northern.tech git projects in `/northern.tech`. Or export
`NT_ROOT` with the path to your base folder.

For example:

```
export NT_ROOT="$HOME/Northern.Tech"
```

CFEngine projects in `/northern.tech/cfengine` (similar for mender, and so on.)
The reason to place it at root is so it can have the same absolute path on all VMs, using a mounted shared folder.
It is not a strict requirement, it's just easier.
If you use another path, you will have to update Vagrantfile and bash scripts.

Something like this does the job:
```
$ export NT_ROOT=/northern.tech
$ sudo mkdir -p $NT_ROOT/cfengine
$ cd $NT_ROOT/cfengine
$ git clone git@github.com:cfengine/starter_pack.git
$ bash ./starter_pack/repos/clone.sh
$ cd starter_pack
```

**Note:** The `clone.sh` script clones all CFEngine repos into the current directory

### SSH keys

```
bash keygen.sh
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
$ sudo su
$ cd /northern.tech/cfengine/core
$ make -j2 install
$ cd ../masterfiles
$ make -j2 install
$ /var/cfengine/bin/cf-key
$ /var/cfengine/bin/cf-agent --bootstrap 192.168.80.90
```

#### Client
```
$ vagrant up client
$ vagrant ssh client
$ sudo su
$ cd /northern.tech/cfengine/core
$ make -j2 install
$ /var/cfengine/bin/cf-key
$ /var/cfengine/bin/cf-agent --bootstrap 192.168.80.90
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

Using `cfbuilder.py`:
```
$ vagrant up dev
$ vagrant ssh dev
$ cd /northern.tech/cfengine/starter_pack
$ python3 cfbuilder.py --autogen --make --core --masterfiles --enterprise --nova
```

The individual steps:
```
$ python3 cfbuilder.py --build-all --dry-run

These commands would run if you didn't specify --dry-run:
cd /northern.tech/cfengine && cd core && ./autogen.sh --enable-debug
cd /northern.tech/cfengine && cd core && make -j2
cd /northern.tech/cfengine && cd enterprise && ./autogen.sh --enable-debug
cd /northern.tech/cfengine && cd enterprise && make -j2
cd /northern.tech/cfengine && cd nova && ./autogen.sh --enable-debug --with-postgresql-hub=/usr
cd /northern.tech/cfengine && cd nova && make -j2
```
(You can run the steps without using `cfbuilder.py`, simplify the `cd` commands if you'd like)

### WIP! Installing CFEngine on hub machine

In general, don't install on your dev machine, and don't run sudo commands on the dev machine.
Everything you're doing there should work without sudo.
Use the `hub` and `client` machines to install and bootstrap.

After compiling on `dev` machine, use `cfbuilder.py` to install on `hub`:
```
$ vagrant up hub
$ vagrant ssh hub
$ sudo su
$ cd /northern.tech/cfengine/starter_pack
$ python3 cfbuilder.py --install --all-repos
$ /var/cfengine/bin/cf-key
$ bash initdb.sh
$ /var/cfengine/bin/cf-agent --bootstrap 192.168.80.90
```

### WIP! Running no-install reporting test
