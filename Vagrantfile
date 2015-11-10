# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # config.vm.provision "shell", path: "pg_config.sh"

  # config.vm.box = "hashicorp/precise32"
  config.vm.box = "ubuntu/trusty64"

  # change/ensure the default route via the local network's WAN router,
  # config.vm.network "public_network", bridge: "en0", ip: "192.168.1.36"

  config.vm.network "forwarded_port", guest: 7001, host: 7001
  # config.vm.network "forwarded_port", guest: 5432, host: 5432
  # config.vm.network "forwarded_port", guest: 8080, host: 8080
end
