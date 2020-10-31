# Dockerfile for apache2 tlspool module
#
# This is arpa2/wip-apachemod_arpa2.
#
# From: Henri Manson <hfmanson@gmail.com>

# start inside build-apachemod with:
# mkdir -p apachemod.git; docker run --rm --name apache -p 8000:80 --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --mount type=bind,source="$(pwd)"/apachemod.git,target=/usr/local/src/apachemod.git -it build-apachemod bash

# ARPA2 base image is build-tlspool
FROM arpa2/build-tlspool AS apache


# Install the Apache tool chain and compile

RUN apt-get install -y automake libtool-bin libpcre3-dev liblmdb-dev lmdb-utils apache2-dev apache2-utils apache2 sasl2-bin

# Install libarpa2common

RUN cd /usr/local/src ; git clone https://gitlab.com/arpa2/libarpa2common.git && \
    cd libarpa2common && git reset v0.7.2 && \
    mkdir build && cd build && \
    cmake .. -D_have_lmdb:INTERNAL=0 && \
    make && \
    make install && \
    ldconfig

# Copy apache resources
# HTML files
COPY /var/www/html /var/www/html
# configuration files
COPY /etc/apache2 /etc/apache2

# prepare sasldb2
RUN echo 1234 | saslpasswd2 -f /etc/sasldb2 -u test-realm.nl henri && \
	chown www-data:www-data /etc/sasldb2

COPY setup-volume.sh /root
RUN echo '. /root/setup-volume.sh' >> /root/.bashrc
CMD ["/bin/bash"]
