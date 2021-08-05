FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update \
 && apt-get -y upgrade \
 && apt-get -y install curl xz-utils telnet
ENV NODEV=v14.17.4
ENV NODE=node-${NODEV}-linux-x64
WORKDIR /usr/local
RUN curl https://nodejs.org/dist/${NODEV}/${NODE}.tar.xz | tar xJ
RUN ln  -s  ${NODE} node
RUN cd bin ; ln -s ../node/bin/* .
RUN npm install -g ganache-cli
RUN cd bin ; ln -s ../node/bin/ganache-cli .
RUN apt-get -y install python3-pip python3.9-dev
RUN python3.9 -m pip install web3 docopt
RUN curl -L https://github.com/ethereum/solidity/releases/download/v0.8.6/solc-static-linux >/usr/local/bin/solc
RUN chmod +x /usr/local/bin/solc
EXPOSE 8545
