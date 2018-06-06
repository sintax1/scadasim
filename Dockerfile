FROM ubuntu:latest

# Add http proxies so container can download packages
ENV http_proxy=http://apcwebproxy.secure.root9b.com:3128
ENV https_proxy=http://apcwebproxy.secure.root9b.com:3128
ENV no_proxy=stash.secure.root9b.com

RUN apt-get update && \
    apt-get -y install git python python-pip

RUN git clone http://github.com/sintax1/scadasim.git

WORKDIR /scadasim

RUN make

COPY scadasim_config.yml scadasim_config.yml

ENTRYPOINT python -i run.py -c scadasim_config.yml

