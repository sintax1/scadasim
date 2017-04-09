FROM ubuntu:latest

RUN apt-get update && \
    apt-get -y install git python python-pip

RUN git clone http://stash.secure.root9b.com/scm/dev/scadasim.git

WORKDIR /scadasim

RUN make

COPY scadasim_config.yml scadasim_config.yml

ENTRYPOINT python -i run.py -c scadasim_config.yml -d

