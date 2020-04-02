# Building support for freeDiameter

> *We have several uses for Diameter, and freeDiameter appears
> to be useful to us.  It is implemented in C, which may be
> helpful for integration with other software.*

Diameter is **realm crossover technology** due to a few important
changes relative to RADIUS:

  * It is secured through TLS or DTLS or IPsec and emphasis mutual checking
  * It has SRV records to help finding a remote realm's server
  * It has facilities for routing and proxying
  * It uses standardised applications and AVPs, but is also extensible without clashes

FreeDiameter has CMake-based build structures to allow code
support to be attached for any extensions.  This has been done
for several areas of use already.

We can use Diameter in a number of access control scenarios:

  - as a [backend SASL validator](https://tools.ietf.org/html/draft-vanrein-diameter-sasl)
  - to discover [ARPA2 ACL rights](http://donai.arpa2.net/acl.html) with alias discovery
  - to resolve questions about [identity inheritance](http://internetwide.org/blog/2016/12/18/id-6-inheritance.html)

For SASL backends, it will be helpful that we are using
the same language as Cyrus SASL, which we will include here and
support through our extensions.

For wrapping a Diameter SASL backend into applications like an
Apache module, it also seems helpful that this is a toolkit built
in C, not C++ or Erlang.

**See also:**

  * [ARPA2 AVP Registry](http://avp.arpa2.org)
  * [freeDiameter test app](http://www.freediameter.net/trac/wiki/test_app.fdx)
    with [client source](http://www.freediameter.net/trac/browser/freeDiameter/extensions/test_app/ta_cli.c)
    and [server soruce](http://www.freediameter.net/trac/browser/freeDiameter/extensions/test_app/ta_serv.c)
    and [app context](http://www.freediameter.net/trac/browser/freeDiameter/extensions/test_app).  Looks doable to make a SASL variation.

**Quick start**

Terminal 1
```
docker run --rm --name diameter --mount type=bind,source="$(pwd)"/usr/local/src/kip.git,target=/usr/local/src/kip.git --hostname kipsvc.unicorn.demo.arpa2.lab -it build-diameter
kipd 0.0.0.0 9876 /usr/local/src/kip.git/test/bin/unicorn.keytab 1
```
Terminal 2
```
freeDiameterd -dd -c /usr/local/src/kip.git/build/test/bin/fdserver.conf
```

Terminal 3
```
docker exec -it diameter bash
/usr/local/src/kip.git/build/src/fdclient -dd -c /usr/local/src/kip.git/build/test/bin/fdclient.conf
/usr/local/src/kip.git/build/src/fdclient -dd -c /usr/local/src/kip.git/build/test/bin/fdclient.conf -v 6666
```
