from ubuntu

RUN apt-get -y update \
		&& apt-get -y upgrade \
		&& apt-get -y install haskell-platform libqt4-dev libgraphviz-dev \ 
			curl tar make g++

RUN curl -L http://www.gecode.org/download/gecode-5.1.0.tar.gz | tar xz \
		&& cd gecode-5.1.0 \
		&& ./configure --prefix=/usr --disable-examples \
		&& make \
		&& make install

COPY . /root

WORKDIR /root
RUN cabal update \
		&& make build \
		&& make install
