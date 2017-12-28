# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    # Use a custom box:
    # https://scotch.io/tutorials/how-to-create-a-vagrant-base-box-from-an-existing-one
    config.vm.box = "basebox"
    # config.vm.box = "ubuntu/trusty64"

    # Run bootstrap.sh script on first boot:
    config.vm.provision "bootstrap", type: "shell", path: "bootstrap.sh"
    config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
    config.vm.synced_folder "/northern.tech", "/northern.tech", type: "virtualbox"

    # Performace settings for each vm:
    config.vm.provider "virtualbox" do |vb|
        vb.memory = 1024 # 1 GiB of memory
        vb.cpus = 1      # 1 CPU Cores

        # Ensure time synchronization:
        vb.customize [ "guestproperty", "set", :id, "/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold", 1000 ]
    end

    # Main development machine: (No network)
    config.vm.define "dev", primary: true, autostart: false do |dev|
        config.vm.hostname = "DEV"
        config.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 2
        end
    end

    # ============================ BUILD MACHINES: ===========================

    config.vm.define "buildslave", autostart: false do |buildslave|
        config.vm.hostname = "buildslave"
        config.vm.box = "buildslavebox"
        config.vm.synced_folder ".", "/vagrant", type: "virtualbox", disabled: true
        config.vm.synced_folder "~/code/northern.tech", "/northern.tech", type: "virtualbox", disabled: true
        config.vm.network "private_network", ip: "192.168.100.100"
        config.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 2
        end
    end

    # Dedicated mingw compile for windows machine:
    config.vm.define "mingw", primary: false, autostart: false do |mingw|
        config.vm.hostname = "mingw"
        config.vm.network "private_network", ip: "192.168.200.200"
        config.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 2
        end
    end

    # ============================ TEST MACHINES: ============================

    # Hub test machine:
    config.vm.define "hub", autostart: false do |hub|
        config.vm.hostname = "hub"
        config.vm.network "private_network", ip: "192.168.80.90"
    end

    # Client test machine:
    config.vm.define "client", autostart: false do |client|
        config.vm.hostname = "client"
        config.vm.network "private_network", ip: "192.168.80.91"
    end

    # Clean test machine:
    config.vm.define "clean", autostart: false do |clean|
        config.vm.box = "ubuntu/trusty64"
        config.vm.hostname = "clean"
        config.vm.network "private_network", ip: "192.168.80.92"
    end

    # =============================== BASE BOX: ==============================

    # Prepackage a box on disk:
    config.vm.define "basebox", autostart: false do |basebox|
        config.vm.box = "ubuntu/trusty64"
        config.vm.provision "bootstrap", type: "shell", path: "basebox/bootstrap.sh"
        config.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 2
        end
    end

    # Prepackage a box on disk:
    config.vm.define "buildslavebox", autostart: false do |buildslavebox|
        config.vm.box = "ubuntu/trusty64"
        config.vm.provision "bootstrap", type: "shell", path: "buildslave/bootstrap.sh"
        config.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 2
        end
    end
end
