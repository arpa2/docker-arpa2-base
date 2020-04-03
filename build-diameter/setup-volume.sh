#!/bin/sh

DIR="/usr/local/src/kip.git"
if [ ! -d "$DIR"/.git ]; then
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
