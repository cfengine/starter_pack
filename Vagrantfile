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
    # config.vm.box = "ubuntu/bionic64"

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
      dev.vm.hostname = "dev"
      dev.vm.network "private_network", ip: "192.168.100.10"
      dev.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 4
        v.customize ["modifyvm", :id, "--vram", "16"]
      end
      dev.vm.provider :libvirt do |v|
        v.memory = 2048
        v.cpus = 2
      end
    end

    # ============================ BUILD MACHINES: ===========================

    config.vm.define "docbuildslave", autostart: false do |docbuildslave|
      docbuildslave.vm.hostname = "docbuildslave"
      docbuildslave.vm.box = "bento/ubuntu-16.04"
      docbuildslave.vm.synced_folder ".", "/vagrant", disabled: false,
                              rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
      docbuildslave.vm.synced_folder "#{NTECH_ROOT}", "/northern.tech", disabled: false,
                              rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
      docbuildslave.vm.network "private_network", ip: "192.168.100.101"
      docbuildslave.vm.provision "shell",
                          name: "Installing Jekyll and the CFEngine documentation tool-chain",
                          privileged: false,
                          path: "#{NTECH_ROOT}/cfengine/documentation-generator/_scripts/provisioning-install-build-tool-chain.sh"
      docbuildslave.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 4
      end
      docbuildslave.vm.provider :libvirt do |v, override|
        v.memory = 2048
        v.cpus = 2
        override.vm.box = "alxgrh/ubuntu-trusty-x86_64"
      end
    end

    config.vm.define "buildslave", autostart: false do |buildslave|
        buildslave.vm.hostname = "buildslave"
        buildslave.vm.box = "buildslavebox"
        buildslave.vm.synced_folder ".", "/vagrant", disabled: true,
                                rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
        buildslave.vm.synced_folder "#{NTECH_ROOT}", "/northern.tech", disabled: true,
                                rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
        buildslave.vm.network "private_network", ip: "192.168.100.100"
        buildslave.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 4
        end
        buildslave.vm.provider :libvirt do |v|
            v.memory = 2048
            v.cpus = 2
        end
    end

    # Dedicated mingw compile for windows machine:
    config.vm.define "mingw", primary: false, autostart: false do |mingw|
        mingw.vm.hostname = "mingw"
        mingw.vm.network "private_network", ip: "192.168.200.200"
        mingw.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 4
        end
        mingw.vm.provider :libvirt do |v|
            v.memory = 2048
            v.cpus = 2
        end
    end

    # ============================ TEST MACHINES: ============================

    # Hub test machine:
    config.vm.define "hub", autostart: false do |hub|
        hub.vm.hostname = "hub"
        hub.vm.network "private_network", ip: "192.168.100.90"
        hub.vm.network :forwarded_port, guest: 443, host: 9002
    end

    # Client test machine:
    config.vm.define "client", autostart: false do |client|
        client.vm.hostname = "client"
        client.vm.network "private_network", ip: "192.168.100.91"
    end

    # Clean test machine:
    config.vm.define "clean", autostart: false do |clean|
        clean.vm.box = "ubuntu/bionic64"
        clean.vm.hostname = "clean"
        clean.vm.network "private_network", ip: "192.168.100.92"
        clean.vm.provider :libvirt do |v, override|
            override.vm.box = "alxgrh/ubuntu-trusty-x86_64"
        end
    end

    # CentOS build/test machine:
    config.vm.define "centos", autostart: false do |centos|
        centos.vm.box = "centos/7"
        centos.vm.hostname = "centos"
        centos.vm.provision "bootstrap", type: "shell", path: "scripts/centos.sh"
        centos.vm.network "private_network", ip: "192.168.100.93"
    end

    # ============================ DEMO MACHINES: ============================

    # Hub test machine:
    config.vm.define "alice", autostart: false do |alice|
        alice.vm.hostname = "alice"
        alice.vm.network "private_network", ip: "192.168.100.94"
        alice.vm.network :forwarded_port, guest: 443, host: 9002
    end

    # Client test machine:
    config.vm.define "bob", autostart: false do |bob|
        bob.vm.hostname = "bob"
        bob.vm.network "private_network", ip: "192.168.100.95"
    end

    config.vm.define "charlie", autostart: false do |charlie|
        charlie.vm.box = "centos/7"
        charlie.vm.hostname = "charlie"
        charlie.vm.provision "bootstrap", type: "shell", path: "scripts/centos.sh"
        charlie.vm.network "private_network", ip: "192.168.100.96"
    end

    # =============================== BASE BOX: ==============================

    # Prepackage a box on disk:
    config.vm.define "basebox", autostart: false do |basebox|
        basebox.vm.box = "ubuntu/bionic64"
        basebox.vm.provision "bootstrap", type: "shell", path: "basebox/bootstrap.sh"
        basebox.ssh.insert_key = false
        basebox.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 4
        end
        basebox.vm.provider :libvirt do |v, override|
            v.memory = 2048
            v.cpus = 2
            override.vm.box = "alxgrh/ubuntu-trusty-x86_64"
        end
    end

    # Prepackage a box on disk:
    config.vm.define "buildslavebox", autostart: false do |buildslavebox|
        buildslavebox.vm.box = "ubuntu/bionic64"
        buildslavebox.vm.provision "bootstrap", type: "shell", path: "buildslave/bootstrap.sh"
        buildslavebox.ssh.insert_key = false
        buildslavebox.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 4
        end
        buildslavebox.vm.provider :libvirt do |v, override|
            v.memory = 2048
            v.cpus = 2
            override.vm.box = "alxgrh/ubuntu-trusty-x86_64"
        end
    end
end
