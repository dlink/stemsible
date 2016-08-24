# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network :private_network, ip: "192.168.33.22"
  config.vm.synced_folder "../stemsible", "/home/vagrant/stemsible",
                          create: true

  config.vm.provider :virtualbox do |vb|
    vb.memory = "1024"
    vb.name = "stemsible"
  end

  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "config/playbook.yml"
    # Uncomment the line below to get more debug output
    # ansible.verbose = "vv"
  end
end
