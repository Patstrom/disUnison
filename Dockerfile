from ubuntu

RUN apt-get -y update \
		&& apt-get -y upgrade \
		&& apt-get -y install haskell-platform libqt4-dev libgraphviz-dev \
			curl tar make g++ subversion git cmake python python3 python3-pip autoconf vim

WORKDIR /root

# Install LLVM
RUN cd /root \
		&& git clone -b release_38-unison --single-branch https://github.com/unison-code/llvm.git \
		&& mkdir llvm-build; cd llvm-build \
		&& cmake /root/llvm \
		&& cmake --build . \
		&& cmake --build . --target install

# Install Gecode
RUN cd /root \
    && git clone -b release-6.0.0 --single-branch https://github.com/Gecode/gecode.git \
		&& cd gecode \
		&& ./configure --prefix=/usr --disable-examples \
		&& make \
		&& make install


RUN mkdir /root/unison
WORKDIR /root/unison
COPY . .

# Install unison
RUN cd src \
		&& cabal update \
		&& make build \
		&& make install
