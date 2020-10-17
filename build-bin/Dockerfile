# Dockerfile for ARPA2 build preparation (binutils)
#
# This is arpa2/buildphase-binutils -- an image based
# on debian:stable via arpa2/base and enhanced with
# software that we use to build ARPA2 binaries.
#
# Other layers can include this one as their basis,
# do some building and restart with another FROM that
# then copies from the build phase.  Tag this image
# arpa2/buildphase-binutils to match with the FROM
# of such preparing build phases.
#
# See:
# https://docs.docker.com/develop/develop-images/multistage-build/
#
# From: Rick van Rein <rick@openfortress.nl>


# ARPA2 base image is the moving target Debian Stable
FROM arpa2/base

# Install required packages
RUN \
    apt-get update && \
    apt-get -y upgrade

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get install -y \
	build-essential \
	git vim nano man tmux \
	flex bison \
	rsyslog strace gdb \
	cmake cmake-curses-gui pkg-config \
	libldap-dev libsasl2-dev libkrb5-dev
	#TODO# runit
	#TODO#libgnutls-dev

# Install ARPA2CM
#ADD https://gitlab.com/arpa2/arpa2cm/-/archive/v0.8.0/arpa2cm-v0.8.0.tar.gz /root/arpa2cm-version-0.8.tar.gz
#RUN cd /usr/local/src && tar -xzvf /root/arpa2cm-version-0.8.tar.gz
#RUN cd /usr/local/src/arpa2cm-v0.8.0 && mkdir build && cd build && cmake .. && make all install
RUN cd /usr/local/src && git clone https://gitlab.com/arpa2/arpa2cm.git
RUN cd /usr/local/src/arpa2cm && mkdir build && cd build && cmake .. && make all install


#RUNIT## Install runit-docker (base already holds runit but not activated)
#RUNIT# RUN git clone https://github.com/arpa2/runit-docker /usr/local/src/runit-docker.git
#RUNIT# RUN make -C /usr/local/src/runit-docker.git install
#RUNIT# COPY service/ /etc/service/

# Define default command
CMD ["/bin/bash"]

#RUNIT# Use runit-docker as the entrypoint
#RUNIT# ENTRYPOINT ["/sbin/runit-docker"]
