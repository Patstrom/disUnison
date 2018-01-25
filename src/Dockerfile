from ubuntu

RUN apt-get -y update \
		&& apt-get -y upgrade \
		&& apt-get -y install haskell-platform libqt4-dev libgraphviz-dev \
			curl tar make g++ subversion

WORKDIR /root

# Install Gecode
RUN svn --non-interactive --no-auth-cache --trust-server-cert \
				--username anonymous --password anonymous@kth.se \
				checkout -r16327 https://svn.gecode.org/svn/gecode/trunk \
		&& cd trunk \
		&& ./configure --prefix=/usr --disable-examples \
		&& make \
		&& make install

RUN mkdir unison
WORKDIR /root/unison
COPY . .

# Install unison
RUN cabal update \
		&& make build \
		&& make install
