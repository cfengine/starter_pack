# CFEngine starter pack

CFEngine enterprise can be pretty hard/tedious to build, because of many repos and dependencies.
This is an attempt to make it easier for new developers.

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
Have all your Northern.tech git projects in `/northern.tech`.
CFEngnine projects in `/northern.tech/cfengine` (similar for mender, and so on.)
The reason to place it at root is so it can have the same absolute path on all VMs, using a mounted shared folder.
It is not a strict requirement, it's just easier.
If you use another path, you will have to update Vagrantfile and bash scripts.

Something like this does the job:
```
$ sudo mkdir /northern.tech
$ sudo mkdir /northern.tech/cfengine
$ cd /northern.tech/cfengine
$ git clone git@github.com:olehermanse/cfengine_starter_pack.git
$ mv cfengine_starter_pack starter_pack
$ bash /northern.tech/cfengine/starter_pack/repos/clone.sh
$ cd /northern.tech/cfengine/starter_pack
```

**Note:** The `clone.sh` script clones all CFEngine repos into the current directory

## Getting started with the dev machine
The development machine has all development libraries already installed.
It is ready to run autogen, make etc.
It will **NOT** work with `build-remote`.
(See the sections on the build machine below.)

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

### Compiling CFEngine Community in the development machine
```
$ vagrant ssh dev
$ cd /northern.tech/cfengine/core
$ ./autogen.sh --enable-debug
$ make -j2
```

### Installing CFEngine Community on a test machine
Hub:
```
$ vagrant up hub
$ vagrant ssh hub
$ cd /northern.tech/cfengine/core
$ make -j2 install
$ sudo /var/cfengine/bin/cf-agent --bootstrap 192.168.10.10
```

Client:
```
$ vagrant up client
$ vagrant ssh client
$ cd /northern.tech/cfengine/core
$ make -j2 install
$ sudo /var/cfengine/bin/cf-agent --bootstrap 192.168.10.10
```

## WIP! Getting started with the build machine

### Creating a build base box
```
$ bash ./buildbox/create.sh
```

### Starting the build machine
```
$ vagrant up build
```

### Testing ssh for build-remote
```
$ ssh build@localhost
$ exit
```
(Should not ask for password)

### Running build-remote
```
$ cd /northern.tech/cfengine/buildscripts
$ bash build-remote --source /northern.tech/cfengine/ build@localhost
```
**This does not work yet!**
