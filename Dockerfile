FROM ubuntu:21.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install apt-utils
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install apt-utils
RUN apt-get -y install curl xz-utils telnet tree python3-pip
WORKDIR /usr/local
RUN curl -L https://github.com/ethereum/solidity/releases/download/v0.8.6/solc-static-linux >bin/solc
RUN curl -L https://github.com/ethereum/solidity/releases/download/v0.7.6/solc-static-linux >bin/solc-0.7.6
RUN chmod +x bin/solc*
ENV NODEV=v14.17.4
ENV NODE=node-${NODEV}-linux-x64
RUN curl https://nodejs.org/dist/${NODEV}/${NODE}.tar.xz | tar xJ
RUN ln  -s  ${NODE} node
RUN cd bin ; ln -s ../node/bin/* .
RUN npm install -g ganache-cli
RUN cd bin ; ln -s ../node/bin/ganache-cli .
ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt && rm requirements.txt
WORKDIR /root/src
EXPOSE 8545
