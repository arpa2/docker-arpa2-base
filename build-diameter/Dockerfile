# build-diameter downloads and builds FreeDiameter
#
# We can use Diameter in a number of access control scenarios:
#  - as a backend SASL validator
#  - to discover ARPA2 ACL rights and unfolding aliases
#  - to resolve identity inheritance questions
#
# From: Rick van Rein <rick@openfortress.nl>


FROM arpa2/build-bin

RUN apt-get update && \
    apt-get install -y libssl-dev libunbound-dev python3-setuptools python3-dev freediameter libfreediameter-dev
RUN python3 /usr/lib/python3/dist-packages/easy_install.py six pyparsing asn1ate

# Quick-DER
RUN git clone https://github.com/vanrein/quick-der /usr/local/src/quick-der.git
RUN mkdir /usr/local/src/quick-der.git/build ; cd /usr/local/src/quick-der.git/build ; cmake -DDEBUG:BOOL=OFF ..	
RUN make -C /usr/local/src/quick-der.git/build all install	
RUN python /usr/local/src/quick-der.git/setup.py install	
RUN python -m easy_install arpa2.quickder_tools	
RUN python -m easy_install arpa2.quickder	

# Install hexio -- TODO: Temporary branch with experimental derdump.quickder
RUN cd /usr/local/src ; git clone -b quick-derdump --single-branch \
		https://github.com/vanrein/hexio hexio.git
RUN cd /usr/local/src/hexio.git ; make hexin hexout ; install hexin hexout /usr/local/bin
RUN cp /usr/local/src/hexio.git/README.MD /HEXIO.MD

COPY setup-volume.sh /root

ADD README.MD /KIP.MD

ENV KIP_REALM=unicorn.demo.arpa2.org

RUN echo '. /root/setup-volume.sh' >> /root/.bashrc
CMD ["bash"]
