$script = <<SCRIPT
    locale-gen en_GB.UTF-8
    apt-add-repository ppa:fish-shell/release-2
    apt-get --assume-yes update
    apt-get --assume-yes dist-upgrade
    apt-get --assume-yes install fish
    chsh -s /usr/bin/fish vagrant

    ln -s /vagrant/vantage /usr/local/bin/vantage
    ln -s /vagrant/vantage /usr/local/bin/vg
SCRIPT

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.provision "shell", inline: $script
end
