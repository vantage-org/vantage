$script = <<SCRIPT
locale-gen en_GB.UTF-8
apt-get --assume-yes update
apt-get --assume-yes upgrade
SCRIPT

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.provision "shell", inline: $script
end
