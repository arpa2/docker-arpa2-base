#!/bin/sh

DIR="/usr/local/src/kip.git"
if [ $$ == 1 ]; then
	if [ ! -d "$DIR"/.git ]; then
		rm -r $DIR/*
		git clone -b sxover-diameter https://gitlab.com/arpa2/kip $DIR
		mkdir $DIR/build
		cd $DIR/build
		cmake -DDEBUG:BOOL=ON ..
		make
		#cd $DIR/build ; ctest
	fi
	make -C $DIR/build install
	mkdir -p /etc/unbound
	cp $DIR/test/bin/root.key /etc/unbound/root.key
	cp $DIR/build/src/kip  /usr/local/bin/kip
	cp $DIR/build/src/kipd /usr/local/bin/kipd
fi
