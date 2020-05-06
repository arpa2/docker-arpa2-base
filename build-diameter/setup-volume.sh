#!/bin/sh

DIR="/usr/local/src/kip.git"
if [ $$ == 1 ]; then
	if [ ! -d "$DIR"/.git ]; then
		rm -r $DIR/*
		git clone -b sxover-diameter-win https://gitlab.com/arpa2/kip $DIR
		mkdir $DIR/build
		cd $DIR/build
		cmake -DDEBUG:BOOL=OFF ..
		make
		#cd $DIR/build ; ctest
	fi
	make -C $DIR/build install
	mkdir -p /etc/unbound
	cp $DIR/test/bin/root.key /etc/unbound/root.key
	cp $DIR/build/src/kip  /usr/local/bin/kip
	cp $DIR/build/src/kipd /usr/local/bin/kipd
	# apache module
	cd $DIR/contrib/apache-modules/arpa2_sxover && apxs -i -a -c mod_arpa2_sxover.c -lsasl2 -lpcre
	# browser plugin
	# Setup the native messaging plugin; you will need to set it up yourself
	mkdir -p ~/.mozilla/native-messaging-hosts && cat $DIR/contrib/browser-plugin/sasl.json | sed 's/@@NATIVE_DIR@@/\/usr\/local\/src\/kip.git/' > ~/.mozilla/native-messaging-hosts/sasl.json
fi
