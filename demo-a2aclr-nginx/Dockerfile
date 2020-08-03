# ARPA2 Resource ACL nginx demo
#
# In this container you can test nginx with a resource acl policy

FROM arpa2/build-bin

COPY README.md /README.md

COPY .bashrc /root

RUN apt-get update && apt-get install -y curl libpcre3-dev zlib1g-dev nodejs

RUN mkdir /usr/local/demo-a2aclr-nginx && \
	cd /usr/local/demo-a2aclr-nginx && \
	git clone https://gitlab.com/arpa2/libarpa2common.git && \
	cd libarpa2common && \
	git checkout v0.7.1 && \
	echo ok && \
	mkdir build && \
	cd build && \
	cmake .. && \
	make && \
	make install && \
	ldconfig && \
	cd /usr/local/demo-a2aclr-nginx && \
	git clone https://gitlab.com/arpa2/nginx-auth-a2aclr.git && \
	curl -O https://nginx.org/download/nginx-1.19.1.tar.gz && \
	tar zxf nginx-1.19.1.tar.gz && \
	cd nginx-1.19.1 && \
	./configure --with-compat \
	    --with-cc-opt="-O0 -I/usr/local/demo-a2aclr-nginx/libarpa2common/src -I/usr/local/demo-a2aclr-nginx/nginx-auth-a2aclr/" \
	    --with-ld-opt="-L/usr/local/lib" \
	    --add-dynamic-module="/usr/local/demo-a2aclr-nginx/nginx-auth-a2aclr" && \
	make && \
	make modules && \
	make install

RUN mkdir -p /srv/trucktyres.example/tyres && \
	mkdir -p /srv/empty

COPY demopolicy /
COPY nginx.conf /
COPY crudapp /usr/local/bin
