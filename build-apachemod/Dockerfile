# Dockerfile for apache2 tlspool module
#
# This is arpa2/wip-apachemod_arpa2.
#
# From: Henri Manson <hfmanson@gmail.com>


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

#COPY setup-volume.sh /root

# Build Apache modules
COPY modules  /usr/local/src/modules

# Copy apache resources
# HTML files
COPY /var/www/html /var/www/html
# configuration files
COPY /etc/apache2 /etc/apache2

RUN cd /usr/local/src/modules/arpa2_userdir && apxs -i -a -c mod_arpa2_userdir.c
RUN cd /usr/local/src/modules/arpa2_aclr    && apxs -i -a -c mod_arpa2_aclr.c \
                                                -larpa2aclr
RUN cd /usr/local/src/modules/arpa2_tlspool && apxs -i -a -c mod_arpa2_tlspool.c \
                                                -ltlspool
RUN cd /usr/local/src/modules/arpa2_sasl && apxs -i -a -c mod_arpa2_sasl.c \
                                                -lsasl2 -lpcre

# Define default command
CMD ["/bin/bash"]
