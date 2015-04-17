$script = <<SCRIPT
    locale-gen en_GB.UTF-8
    apt-get --assume-yes update
    apt-get --assume-yes upgrade

    wget -qO- https://get.docker.com/ | sh
    usermod -aG docker vagrant

    echo "VG_PLUGIN_PATH=/vagrant/plugins:/vagrant/dogfood" >> /etc/environment
    echo "VG_APP_DIR=/vagrant" >> /etc/environment
    ln -s /vagrant/vantage /usr/local/bin/vantage
    ln -s /vagrant/vantage /usr/local/bin/vg
SCRIPT

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.provision "shell", inline: $script
end
