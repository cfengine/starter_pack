# CFEngine starter pack

CFEngine enterprise can be pretty hard/tedious to build, because of many repos and dependencies.
This is an attempt to make it easier for new developers.

## Installing vagrant and virtualbox

It is recommended, but not required, to run builds and tests inside VMs managed by vagrant.

Install virtualbox:
https://www.virtualbox.org/

Install vagrant:
https://www.vagrantup.com/docs/installation/

(If you know how to use libvirt/kvm or other virtualization software, feel free to use that).

## Getting started

### Installing dependencies (creating a base box)

The vagrant VMs use a custom base box where some dependencies are installed.
To create this box locally, run:
```
./basebox/create.sh
```
(vagrant required).
This will run commands from `basebox/bootstrap.sh` on an Ubuntu VM. 
If you're not using vagrant, you can run/adapt that script on a build/development machine of your choice.

### Cloning CFEngine repositories

All CFEngine repositories should be placed side by side in the same folder on your machine.

This can be done using the `repos/clone.sh` script:
```
$ ./cfengine_starter_pack/repos/clone.sh 
Cloning into 'core'...
remote: Counting objects: 116067, done.
remote: Compressing objects: 100% (26/26), done.
remote: Total 116067 (delta 9), reused 10 (delta 1), pack-reused 116040
Receiving objects: 100% (116067/116067), 53.73 MiB | 2.47 MiB/s, done.
Resolving deltas: 100% (89170/89170), done.
enterprise already exists
nova already exists
mission-portal already exists
buildscripts already exists
documentation already exists
documentation-generator already exists
```
This will clone all repos into current working directory.
Directories which already exist will be skipped, not overwritten(!).
(Valid ssh key with access to private repos needed on machine).
