# Dockerfile for ARPA2 base image
#
# This is arpa2/base -- an image based on debian:stable and
# enhanced with software that we generally use within the
# ARPA2 projects.
#
# It defines a default ENTRYPOINT based on dumb-init to
# allow you to just specify a CMD that will run if you
# start the container.  Signals are caught by PID 1 and
# propagated to your programs.
#
# From: Rick van Rein <rick@openfortress.nl>


# ARPA2 base image is the latest Debian Stable that we have tested and is known
# to fully work with all demos.
#
# As soon as a new release of Debian Stable comes out, please test and
# coordinate this with the owners of the different demos so that we can plan an
# upgrade moment of our own choosing without being strictly dictated by the release
# schedule of Debian and the inevitable period of non-working demos right after
# a new Debian release.
#
# From a security point of view: a new stable is released every two years and
# each stable gets security patches for the most popular packages for five years
# so that would give us plenty of time to keep tracking stable without ever
# breaking our demos.
FROM debian:stretch

# Install required packages
RUN \
    apt-get update && \
    apt-get -y upgrade

# ENV DEBIAN_FRONTEND=noninteractive

ADD krb5.conf /etc/krb5.conf
# ADD selections.debconf /tmp/selections.debconf
# RUN debconf-set-selections /tmp/selections.debconf

#NO_MORE_INIT# RUN apt-get install -y dumb-init runit ca-certificates krb5-user openldap-utils ldapvi nano procps less lrzsz net-tools netcat python3 python3-setuptools
RUN apt-get install -y ca-certificates krb5-user openldap-utils ldapvi nano procps less lrzsz net-tools netcat python3 python3-setuptools

RUN ln -s /bin/nano        /usr/bin/vi && \
    ln -s /usr/bin/python3 /usr/bin/python

ADD sharetty /usr/bin/sharetty
ADD https://github.com/anishathalye/seashells/archive/v0.1.2.tar.gz /usr/local/src/seashells-0.1.2.tar.gz
RUN cd /usr/local/src ; tar -xzvf seashells-0.1.2.tar.gz

ADD arpa2shell /usr/bin/arpa2shell
ADD arpa2cmd.py /usr/lib/python3/dist-packages/arpa2cmd.py
# ADD readline.py /usr/lib/python3/dist-packages/readline.py

# Add files relative to this Dockerfile
# ADD index.html /var/www/index.html

# Set environment variables
# ENV HOME /var/www

# Define working directory
# WORK /var/www

# Install the ARPA2 install / daemon / shell startup context
ADD usr-arpa2-bin /usr/arpa2/bin
RUN mkdir -p /var/arpa2
RUN echo base > /var/arpa2/docker.name
RUN echo /usr/arpa2/bin/docker.go >> /root/.bash_login

# Your default command could be anything beyond a shell
CMD [ "/usr/arpa2/bin/docker.go" ]

# Vim is quickly becoming unusable.  Be conservative to at least be stable.
COPY vimrc /root/.vimrc

# Define default entry point via dumb-init
# ENTRYPOINT [ "/usr/bin/dumb-init", "-v", "--" ]
#NO_MORE_INIT# ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]
#NO_MORE_INIT# #STUCK-PITTY# ENTRYPOINT [ "/sbin/runit-init" ]
