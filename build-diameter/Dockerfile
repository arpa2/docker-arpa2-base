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

RUN mkdir /etc/unbound

ADD README.MD /KIP.MD

ENV KIP_REALM=unicorn.demo.arpa2.org
RUN cp /etc/hosts /tmp/hosts ; sed -i "\${s/\$/a kipsvc.unicorn.demo.arpa2.lab/}" /tmp/hosts ; echo 'cp /tmp/hosts /etc/hosts' >> /root/.bashrc
CMD ["bash"]
