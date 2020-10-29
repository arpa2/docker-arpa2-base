# README for the ARPA2 Apache Modules #

> *These modules link the Apache Web Server to a number of ARPA2 projects.*

# General setup #

## Starting ##
```
$ docker run --rm --name apache -p 8000:80 -it build-apachemod bash
```
## Inside docker ##
```
root@9b0050a13502:/# /etc/init.d/rsyslog start
root@9b0050a13502:/# tlspool-daemon -kc /etc/tlspool.conf
root@9b0050a13502:/# apachectl start
```
## On PC: prepare /etc/hosts ##
```
127.0.0.1       localhost tlspool.arpa2.lab playground.arpa2.lab
127.0.1.1       ingrid-linux

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```
# ACLR demo, inside docker #
```
root@9b0050a13502:/# a2dismod sasl
```
## On PC in docker-demo directory ##
```
$ docker cp apache:/usr/local/src/tlspool-0.9.3/testdata/tlspool-test-ca-cert.pem build-apachemod
manson@manson-Satellite-L300:~/docker/docker-demo$ curl --cacert build-apachemod/tlspool-test-ca-cert.pem -v -u hfmanson@localhost:henri1234 https://tlspool.arpa2.lab:8000/
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to tlspool.arpa2.lab (127.0.0.1) port 8000 (#0)
* ALPN, offering h2
* ALPN, offering http/1.1
* successfully set certificate verify locations:
*   CAfile: build-apachemod/tlspool-test-ca-cert.pem
  CApath: /etc/ssl/certs
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
* TLSv1.3 (IN), TLS handshake, Unknown (8):
* TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
* TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
* TLSv1.3 (IN), TLS handshake, Finished (20):
* TLSv1.3 (OUT), TLS change cipher, Client hello (1):
* TLSv1.3 (OUT), TLS Unknown, Certificate Status (22):
* TLSv1.3 (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* ALPN, server did not agree to a protocol
* Server certificate:
*  subject: CN=TLS Pool Test X.509 Webhost Server; OU=Test Servers; O=ARPA2 Laboratories; L=Internet; ST=Freedom
*  start date: Mar  3 13:22:31 2020 GMT
*  expire date: May 12 13:22:31 2020 GMT
*  subjectAltName: host "tlspool.arpa2.lab" matched cert's "tlspool.arpa2.lab"
*  issuer: CN=TLS Pool Test CA; OU=Testing Unit; O=ARPA2 Laboratories; L=Internet; ST=Freedom
*  SSL certificate verify ok.
* Server auth using Basic with user 'hfmanson@localhost'
* TLSv1.3 (OUT), TLS Unknown, Unknown (23):
> GET / HTTP/1.1
> Host: tlspool.arpa2.lab:8000
> Authorization: Basic aGZtYW5zb25AbG9jYWxob3N0OmhlbnJpMTIzNA==
> User-Agent: curl/7.58.0
> Accept: */*
>
* TLSv1.3 (IN), TLS Unknown, Unknown (23):
< HTTP/1.1 200 OK
< Date: Wed, 04 Mar 2020 16:51:31 GMT
< Server: Apache/2.4.38 (Debian)
< Last-Modified: Wed, 04 Mar 2020 16:45:35 GMT
< ETag: "3d-5a00a2639e9c0"
< Accept-Ranges: bytes
< Content-Length: 61
< Content-Type: text/html
<
<html><body><h1>tlspool.arpa2.lab, SECRET</h1></body></html>
* Connection #0 to host tlspool.arpa2.lab left intact
manson@manson-Satellite-L300:~/docker/docker-demo$ curl --cacert build-apachemod/tlspool-test-ca-cert.pem -v https://playground.arpa2.lab:8000/
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to playground.arpa2.lab (127.0.0.1) port 8000 (#0)
* ALPN, offering h2
* ALPN, offering http/1.1
* successfully set certificate verify locations:
*   CAfile: build-apachemod/tlspool-test-ca-cert.pem
  CApath: /etc/ssl/certs
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
* TLSv1.3 (IN), TLS handshake, Unknown (8):
* TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
* TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
* TLSv1.3 (IN), TLS handshake, Finished (20):
* TLSv1.3 (OUT), TLS change cipher, Client hello (1):
* TLSv1.3 (OUT), TLS Unknown, Certificate Status (22):
* TLSv1.3 (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* ALPN, server did not agree to a protocol
* Server certificate:
*  subject: CN=TLS Pool Test X.509 Playground Server; OU=Test Servers; O=ARPA2 Laboratories; L=Internet; ST=Freedom
*  start date: Mar  3 13:22:31 2020 GMT
*  expire date: May 12 13:22:31 2020 GMT
*  subjectAltName: host "playground.arpa2.lab" matched cert's "playground.arpa2.lab"
*  issuer: CN=TLS Pool Test CA; OU=Testing Unit; O=ARPA2 Laboratories; L=Internet; ST=Freedom
*  SSL certificate verify ok.
* TLSv1.3 (OUT), TLS Unknown, Unknown (23):
> GET / HTTP/1.1
> Host: playground.arpa2.lab:8000
> User-Agent: curl/7.58.0
> Accept: */*
>
* TLSv1.3 (IN), TLS Unknown, Unknown (23):
< HTTP/1.1 200 OK
< Date: Wed, 04 Mar 2020 16:52:10 GMT
< Server: Apache/2.4.38 (Debian)
< Last-Modified: Wed, 08 Jan 2020 12:01:42 GMT
< ETag: "38-59b9fa7ddf580"
< Accept-Ranges: bytes
< Content-Length: 56
< Content-Type: text/html
<
<html><body><h1>playground.arpa2.lab</h1></body></html>
* Connection #0 to host playground.arpa2.lab left intact
manson@manson-Satellite-L300:~/docker/docker-demo$
```

## Inside docker ##
```
root@9b0050a13502:/# tail -n 5 /usr/local/apache2/logs/error_log 
[Wed Mar 04 16:51:31.062563 2020] [tlspool:notice] [pid 52:tid 140509049779968] AH03297: tlspool_pre_connection: c = 7fcad7ebb348, pool = 7fcad7ebb028, old = 11, nVerifyCLient = 0, flags = 0x00011006
[Wed Mar 04 16:51:31.117659 2020] [tlspool:notice] [pid 52:tid 140509049779968] AH03297: tlspool_pre_connection: new = 13, localid = tlspool.arpa2.lab
[Wed Mar 04 16:51:31.119785 2020] [aclr:notice] [pid 52:tid 140509049779968] AH03297: x_check_authz(): user = hfmanson@localhost, uri = /, realm = myrealm, ap_auth_type = Basic, method = GET
[Wed Mar 04 16:51:31.119827 2020] [aclr:notice] [pid 52:tid 140509049779968] AH03297: looking up R in /etc/apache2/aclrpolicy, ctx: 559340689e50
[Wed Mar 04 16:51:31.119859 2020] [aclr:notice] [pid 52:tid 140509049779968] AH03297: R: PERMITTED
```
