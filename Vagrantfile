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
    # config.vm.box = "ubuntu/focal64"

    # make sure SSH always has host keys
    config.vm.provision "ssh-host-keys", type: "shell", path: "scripts/ssh-host-keys.sh"

    # Enable using normal ssh command by copying your normal SSH key into VM:
    config.vm.provision "shell" do |s|
      ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_rsa.pub").first.strip
      s.inline = <<-SHELL
        echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys
        echo #{ssh_pub_key} >> /root/.ssh/authorized_keys
      SHELL
    end

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

    # Synchonize clock with host OS to avoid clock skew when using tools like
    # Make and rsync. Only do this if "vagrant-timezone" plugin is installed.
    if Vagrant.has_plugin?("vagrant-timezone")
        config.timezone.value = :host
    end

    # https://bugs.launchpad.net/cloud-images/+bug/1874453
    NOW = Time.now.strftime("%d.%m.%Y.%H:%M:%S")
    FILENAME = "serial-debug-%s.log" % NOW
    config.vm.provider "virtualbox" do |vb|
       vb.customize [ "modifyvm", :id, "--uart1", "0x3F8", "4" ]
       vb.customize [ "modifyvm", :id, "--uartmode1", "file",
       File.join(Dir.pwd, FILENAME) ]
    end

    config.vm.provider :libvirt do |v, override|
      v.memory = 1024
      v.cpus = 1
      # Fedora 30+ uses QEMU sessions by default, breaking pretty much all
      # previously working Vagrantfiles:
      # https://fedoraproject.org/wiki/Changes/Vagrant_2.2_with_QEMU_Session#Upgrade.2Fcompatibility_impact
      v.qemu_use_session = false
      override.vm.synced_folder "./", "/vagrant", type: :rsync
      override.vm.synced_folder "#{NTECH_ROOT}", "/northern.tech", type: :rsync
    end

    # Main development machine:
    config.vm.define "dev", primary: true, autostart: false do |dev|
      dev.vm.hostname = "dev"
      dev.vm.network "private_network", ip: "192.168.56.10"
      # Doesn't work in libvirt:
      # dev.vm.network "private_network", ip: "fde4:8dba:82e1::c4"
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
      docbuildslave.vm.synced_folder "#{NTECH_ROOT}", "/northern.tech", disabled: false, type: "rsync",
                              rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
      docbuildslave.vm.network "private_network", ip: "192.168.56.101"
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
        override.vm.box = "generic/ubuntu2004"
      end
    end

    config.vm.define "buildslave", autostart: false do |buildslave|
        buildslave.vm.hostname = "buildslave"
        buildslave.vm.box = "buildslavebox"
        buildslave.vm.synced_folder ".", "/vagrant", disabled: true,
                                rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
        buildslave.vm.synced_folder "#{NTECH_ROOT}", "/northern.tech", disabled: true,
                                rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]
        buildslave.vm.network "private_network", ip: "192.168.56.100"
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
        hub.vm.network "private_network", ip: "192.168.56.90"
        hub.vm.network :forwarded_port, guest: 443, host: 9002
    end

    # Client test machine:
    config.vm.define "client", autostart: false do |client|
        client.vm.hostname = "client"
        client.vm.network "private_network", ip: "192.168.56.91"
    end

    # Clean test machine:
    config.vm.define "clean", autostart: false do |clean|
        clean.vm.box = "ubuntu/focal64"
        clean.vm.hostname = "clean"
        clean.vm.network "private_network", ip: "192.168.56.92"
        clean.vm.provider :libvirt do |v, override|
            override.vm.box = "generic/ubuntu2004"
        end
    end

    # CentOS build/test machine:
    config.vm.define "centos", autostart: false do |centos|
        centos.vm.box = "centos/7"
        centos.vm.hostname = "centos"
        centos.vm.provision "bootstrap", type: "shell", path: "scripts/centos.sh"
        centos.vm.network "private_network", ip: "192.168.56.93"
    end

    # ============================ DEMO MACHINES: ============================

    # Hub test machine:
    config.vm.define "alice", autostart: false do |alice|
        alice.vm.hostname = "alice"
        alice.vm.network "private_network", ip: "192.168.56.94"
        alice.vm.network :forwarded_port, guest: 443, host: 9002
    end

    # Client test machine:
    config.vm.define "bob", autostart: false do |bob|
        bob.vm.hostname = "bob"
        bob.vm.network "private_network", ip: "192.168.56.95"
    end

    config.vm.define "charlie", autostart: false do |charlie|
        charlie.vm.box = "centos/7"
        charlie.vm.hostname = "charlie"
        charlie.vm.provision "bootstrap", type: "shell", path: "scripts/centos.sh"
        charlie.vm.network "private_network", ip: "192.168.56.96"
    end

    # =============================== BASE BOX: ==============================

    # Prepackage a box on disk:
    config.vm.define "basebox", autostart: false do |basebox|
        basebox.vm.box = "ubuntu/focal64"
        basebox.vm.provision "bootstrap", type: "shell", path: "basebox/bootstrap.sh"
        basebox.ssh.insert_key = false
        basebox.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 4
        end
        basebox.vm.provider :libvirt do |v, override|
            v.memory = 2048
            v.cpus = 2
            override.vm.box = "generic/ubuntu2004"
        end
    end

    # Prepackage a box on disk:
    config.vm.define "buildslavebox", autostart: false do |buildslavebox|
        buildslavebox.vm.box = "ubuntu/focal64"
        buildslavebox.vm.provision "bootstrap", type: "shell", path: "buildslave/bootstrap.sh"
        buildslavebox.ssh.insert_key = false
        buildslavebox.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 4
        end
        buildslavebox.vm.provider :libvirt do |v, override|
            v.memory = 2048
            v.cpus = 2
            override.vm.box = "generic/ubuntu2004"
        end
    end
end
