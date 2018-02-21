from ubuntu

RUN apt-get -y update \
		&& apt-get -y upgrade \
		&& apt-get -y install haskell-platform libqt4-dev libgraphviz-dev \
			curl tar make g++ subversion git cmake python autoconf vim

WORKDIR /root

# Install LLVM
RUN cd /root \
		&& git clone -b master-unison --single-branch https://github.com/unison-code/llvm.git \
		&& mkdir llvm-build; cd llvm-build \
		&& cmake /root/llvm \
		&& cmake --build . \
		&& cmake --build . --target install

# Install Gecode
RUN cd /root \
    && svn --non-interactive --no-auth-cache --trust-server-cert-failures=expired,unknown-ca,other \
				--username anonymous --password anonymous@kth.se \
				checkout -r16327 https://svn.gecode.org/svn/gecode/trunk \
		&& cd trunk \
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
