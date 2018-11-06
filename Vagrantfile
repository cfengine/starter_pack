# -*- mode: ruby -*-
# vi: set ft=ruby :

if ENV['NTECH_ROOT']
  NTECH_ROOT=ENV['NTECH_ROOT']
else
  NTECH_ROOT="/northern.tech" # Subfolders: cfengine[, zener]
end

Vagrant.configure("2") do |config|
    # Use a custom box:
    # https://scotch.io/tutorials/how-to-create-a-vagrant-base-box-from-an-existing-one
    config.vm.box = "basebox"
    # config.vm.box = "ubuntu/trusty64"

    # make sure SSH always has host keys
    config.vm.provision "ssh-host-keys", type: "shell", path: "scripts/ssh-host-keys.sh"

    # Run bootstrap.sh script on first boot:
    config.vm.provision "bootstrap", type: "shell", path: "bootstrap.sh"
    config.vm.synced_folder  ".", "/vagrant",
                             rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
    config.vm.synced_folder "#{NTECH_ROOT}", "/northern.tech",
                            rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]

    # Performace settings for each vm:
    config.vm.provider "virtualbox" do |vb|
        vb.memory = 1024 # 1 GiB of memory
        vb.cpus = 1      # 1 CPU Cores

        # Ensure time synchronization:
        vb.customize [ "guestproperty", "set", :id, "/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold", 1000 ]
    end
    config.vm.provider :libvirt do |v, override|
      v.memory = 1024
      v.cpus = 1
      override.vm.synced_folder "./", "/vagrant", type: :rsync
      override.vm.synced_folder "#{NTECH_ROOT}", "/northern.tech", type: :rsync
    end

    # Main development machine:
    config.vm.define "dev", primary: true, autostart: false do |dev|
      config.vm.hostname = "dev"
      config.vm.network "private_network", ip: "192.168.100.10"
      config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 2
        v.customize ["modifyvm", :id, "--vram", "16"]
      end
      config.vm.provider :libvirt do |v|
        v.memory = 2048
        v.cpus = 2
      end
    end

    # ============================ BUILD MACHINES: ===========================

    config.vm.define "docbuildslave", autostart: false do |docbuildslave|
      config.vm.hostname = "docbuildslave"
      config.vm.box = "bento/ubuntu-16.04"
      config.vm.synced_folder ".", "/vagrant", disabled: false,
                              rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
      config.vm.synced_folder "#{NTECH_ROOT}", "/northern.tech", disabled: false,
                              rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
      config.vm.network "private_network", ip: "192.168.100.101"
      config.vm.provision "shell",
                          name: "Installing Jekyll and the CFEngine documentation tool-chain",
                          privileged: false,
                          path: "#{NTECH_ROOT}/documentation-generator/_scripts/provisioning-install-build-tool-chain.sh"
      config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 2
      end
      config.vm.provider :libvirt do |v, override|
        v.memory = 2048
        v.cpus = 2
        override.vm.box = "alxgrh/ubuntu-trusty-x86_64"
      end
    end

    config.vm.define "buildslave", autostart: false do |buildslave|
        config.vm.hostname = "buildslave"
        config.vm.box = "buildslavebox"
        config.vm.synced_folder ".", "/vagrant", disabled: true,
                                rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
        config.vm.synced_folder "#{NTECH_ROOT}", "/northern.tech", disabled: true,
                                rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
        config.vm.network "private_network", ip: "192.168.100.100"
        config.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 2
        end
        config.vm.provider :libvirt do |v|
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
        config.vm.provider :libvirt do |v|
            v.memory = 2048
            v.cpus = 2
        end
    end

    # ============================ TEST MACHINES: ============================

    # Hub test machine:
    config.vm.define "hub", autostart: false do |hub|
        config.vm.hostname = "hub"
        config.vm.network "private_network", ip: "192.168.100.90"
        config.vm.network :forwarded_port, guest: 443, host: 9002
    end

    # Client test machine:
    config.vm.define "client", autostart: false do |client|
        config.vm.hostname = "client"
        config.vm.network "private_network", ip: "192.168.100.91"
    end

    # Clean test machine:
    config.vm.define "clean", autostart: false do |clean|
        config.vm.box = "ubuntu/trusty64"
        config.vm.hostname = "clean"
        config.vm.network "private_network", ip: "192.168.100.92"
        config.vm.provider :libvirt do |v, override|
            override.vm.box = "alxgrh/ubuntu-trusty-x86_64"
        end
    end

    # CentOS build/test machine:
    config.vm.define "centos", autostart: false do |centos|
        config.vm.box = "centos/7"
        config.vm.hostname = "centos"
        config.vm.provision "bootstrap", type: "shell", path: "scripts/centos.sh"
        config.vm.network "private_network", ip: "192.168.100.93"
    end

    # ============================ DEMO MACHINES: ============================

    # Hub test machine:
    config.vm.define "alice", autostart: false do |alice|
        config.vm.hostname = "alice"
        config.vm.network "private_network", ip: "192.168.100.94"
        config.vm.network :forwarded_port, guest: 443, host: 9002
    end

    # Client test machine:
    config.vm.define "bob", autostart: false do |bob|
        config.vm.hostname = "bob"
        config.vm.network "private_network", ip: "192.168.100.95"
    end

    config.vm.define "charlie", autostart: false do |charlie|
        config.vm.box = "centos/7"
        config.vm.hostname = "charlie"
        config.vm.provision "bootstrap", type: "shell", path: "scripts/centos.sh"
        config.vm.network "private_network", ip: "192.168.100.96"
    end

    # =============================== BASE BOX: ==============================

    # Prepackage a box on disk:
    config.vm.define "basebox", autostart: false do |basebox|
        config.vm.box = "ubuntu/trusty64"
        config.vm.provision "bootstrap", type: "shell", path: "basebox/bootstrap.sh"
        config.ssh.insert_key = false
        config.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 2
        end
        config.vm.provider :libvirt do |v, override|
            v.memory = 2048
            v.cpus = 2
            override.vm.box = "alxgrh/ubuntu-trusty-x86_64"
        end
    end

    # Prepackage a box on disk:
    config.vm.define "buildslavebox", autostart: false do |buildslavebox|
        config.vm.box = "ubuntu/trusty64"
        config.vm.provision "bootstrap", type: "shell", path: "buildslave/bootstrap.sh"
        config.ssh.insert_key = false
        config.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 2
        end
        config.vm.provider :libvirt do |v, override|
            v.memory = 2048
            v.cpus = 2
            override.vm.box = "alxgrh/ubuntu-trusty-x86_64"
        end
    end
end
