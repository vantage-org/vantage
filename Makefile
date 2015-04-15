PLUGINHOOK_URL ?= https://s3.amazonaws.com/progrium-pluginhook/pluginhook_0.1.0_amd64.deb

all:
	# Type "make install" to install.

install: dependencies
	if [ ! -d /usr/local/vantage ] ; then cp -r . /usr/local/vantage ; fi
	ln -s /usr/local/vantage/vantage /usr/local/bin/vantage
	ln -s /usr/local/vantage/vantage /usr/local/bin/vg

dependencies: pluginhook docker

pluginhook:
	wget -qO /tmp/pluginhook_0.1.0_amd64.deb ${PLUGINHOOK_URL}
	dpkg -i /tmp/pluginhook_0.1.0_amd64.deb

docker: 
	wget -qO- https://get.docker.com/ | sh
