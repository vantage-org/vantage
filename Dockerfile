FROM ubuntu

RUN apt-get -y update &&\
    apt-get -y dist-upgrade &&\
    apt-get -y install build-essential wget

ADD . /vantage
WORKDIR /vantage

RUN make install

CMD ["bash"]
