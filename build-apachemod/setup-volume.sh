#!/bin/sh

DIR="/usr/local/src/apachemod.git"
if [ $$ == 1 ]; then
	if [ ! -d "$DIR"/.git ]; then
		rm -r $DIR/*
		git clone https://gitlab.com/arpa2/apachemod $DIR
	fi
	cd $DIR/arpa2_userdir
	apxs -i -a -c mod_arpa2_userdir.c
	cd $DIR/arpa2_aclr
	apxs -i -a -c mod_arpa2_aclr.c -larpa2aclr
	cd $DIR/arpa2_tlspool
	apxs -i -a -c mod_arpa2_tlspool.c -ltlspool
	cd $DIR/arpa2_sasl
	apxs -i -a -c mod_arpa2_sasl.c -lsasl2 -lpcre
fi
