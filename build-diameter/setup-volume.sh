#!/bin/sh

rm -r /usr/local/src/kip.git/*
git clone -b sxover-diameter https://gitlab.com/arpa2/kip /usr/local/src/kip.git
mkdir /usr/local/src/kip.git/build
cd /usr/local/src/kip.git/build
cmake ..
make -C /usr/local/src/kip.git/build
cp /usr/local/src/kip.git/test/bin/root.key /etc/unbound/root.key
#cd /usr/local/src/kip.git/build ; ctest
cp /usr/local/src/kip.git/build/src/kip  /usr/local/bin/kip
cp /usr/local/src/kip.git/build/src/kipd /usr/local/bin/kipd
