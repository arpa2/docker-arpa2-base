# Dockerfile for Quick DER and LillyDAP
#
# This is a build environment that sets up two
# small tools that are used under several ARPA2
# projects.
#
# Quick DER is a small and efficient DER parser
# and generator.
#
# LillyDAP is a small and efficient LDAP building
# block.
#
# From: Rick van Rein <rick@openfortress.nl>


# Prepare setuptools for import
#
#UNUSED# FROM arpa2/build-pip AS pip


# Build on top of the ARPA2 build base image
#
FROM arpa2/build-bin

# Install required packages (already done in arpa2/base)
# RUN \
#     apt-get update && \
#     apt-get -y upgrade

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
# RUN apt-get install -y libdb5.3-dev libgnutls28-dev gnutls-bin libldns-dev
RUN apt-get install -y \
	python3-pyparsing python3-six python3-setuptools python3-dev \
	gperf

#UNUSED# COPY --from=pip /usr/lib/python3.7/dist-packages/setuptools/ /usr/lib/python3.7/dist-packages/setuptools
#UNUSED# COPY --from=pip /usr/lib/python3.7/dist-packages/pkg_resources/ /usr/lib/python3.7/dist-packages/pkg_resources

# Install asn1ate
RUN python3 /usr/lib/python3/dist-packages/easy_install.py six pyparsing asn1ate

# Quick-DER
RUN git clone https://gitlab.com/arpa2/quick-der/ /usr/local/src/quick-der.git
RUN mkdir /usr/local/src/quick-der.git/build ; cd /usr/local/src/quick-der.git/build ; cmake -DDEBUG:BOOL=OFF ..	
RUN make -C /usr/local/src/quick-der.git/build all install	
RUN python /usr/local/src/quick-der.git/setup.py install	
RUN python -m easy_install arpa2.quickder_tools	
RUN python -m easy_install arpa2.quickder	

# Install hexio -- TODO: Temporary branch with experimental derdump.quickder
RUN cd /usr/local/src ; git clone -b quick-derdump --single-branch \
		https://github.com/vanrein/hexio hexio.git
RUN cd /usr/local/src/hexio.git ; make hexin hexout ; install hexin hexout derdump derdump.quickder /usr/local/bin
RUN cp /usr/local/src/hexio.git/README.MD /HEXIO.MD

# Install LillyDAP
RUN git clone https://gitlab.com/arpa2/lillydap /usr/local/src/lillydap.git
RUN cd /usr/local/src/lillydap.git && mkdir build && cd build && cmake .. && make all test install

# Trigger library updates
RUN ldconfig

# Define default command
CMD ["/bin/bash"]
