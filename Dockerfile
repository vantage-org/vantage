FROM ubuntu

RUN apt-get -y update && \
    apt-get -y dist-upgrade && \
    apt-get -y install wget git && \
    ln -s /usr/local/vantage/vantage /usr/local/bin/vantage && \
    ln -s /usr/local/vantage/vantage /usr/local/bin/vg

RUN wget -qO- https://get.docker.com/ | sh

ADD . /usr/local/vantage
WORKDIR /usr/local/vantage

ENV VG_APP_DIR /usr/local/vantage

CMD ["bash"]
