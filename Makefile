all:
	# Type "make install" to install.

install: dependencies
	if [ ! -d /usr/local/vantage ] ; then cp -r . /usr/local/vantage ; fi
	ln -s /usr/local/vantage/vantage /usr/local/bin/vantage
	ln -s /usr/local/vantage/vantage /usr/local/bin/vg

dependencies: docker

docker: 
	wget -qO- https://get.docker.com/ | sh
