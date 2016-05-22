$script = <<SCRIPT
    locale-gen en_GB.UTF-8
    apt-get --assume-yes update
    apt-get --assume-yes dist-upgrade
    apt-get --assume-yes install git

    ln -s /vagrant/vantage /usr/local/bin/vantage
    ln -s /vagrant/vantage /usr/local/bin/vg

    mkdir -p /vagrant/.env
    echo "FOO=one" > /vagrant/.env/one
    echo "FOO=two" > /vagrant/.env/two
    chown -R vagrant:vagrant /vagrant/.env
SCRIPT

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.provision "shell", inline: $script
end
