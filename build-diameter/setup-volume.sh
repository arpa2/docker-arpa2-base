#!/bin/sh

git clone https://github.com/vanrein/quick-der /usr/local/src/quick-der.git
mkdir /usr/local/src/quick-der.git/build
cd /usr/local/src/quick-der.git/build
cmake -DDEBUG:BOOL=OFF ..
make -C /usr/local/src/quick-der.git/build all install
python /usr/local/src/quick-der.git/setup.py install
python -m easy_install arpa2.quickder_tools
python -m easy_install arpa2.quickder
git clone -b sxover-diameter https://gitlab.com/arpa2/kip /usr/local/src/kip.git
mkdir /usr/local/src/kip.git/build
cd /usr/local/src/kip.git/build
cmake ..
make -C /usr/local/src/kip.git/build
cp /usr/local/src/kip.git/test/bin/root.key /etc/unbound/root.key
#cd /usr/local/src/kip.git/build ; ctest
cp /usr/local/src/kip.git/build/src/kip  /usr/local/bin/kip
cp /usr/local/src/kip.git/build/src/kipd /usr/local/bin/kipd
