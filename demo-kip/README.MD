# Docker Demo for KIP

> *KIP, the Keyful Identity Protocol, makes encryption really simple.
> Key management is taken care of by a KIP Service, run under your domain.*

The demo runs under a prepared demonstration domain: `unicorn.demo.arpa2.org`
It refers to the Docker container by a funny name: `kipsvc.unicorn.demo.arpa2.lab`
(note the last part!)

.. ![Overview of KIP](kip-overview.png)


## Example KIP file

The file [kip-up-and-down.c](kip-up-and-down.c) uses the library `libkip.so` to
add encryption/integrity (`kip up`) and remove/check it (`kip down`).  The result
of kipping up security is in [kip-up-and-down.kip](kip-up-and-down.kip) which
you could teach your web browser and mail tool to open, some day.


## Building this Docker Image

The standard recipe builds dependencies first:

```
git clone https://github.com/arpa2/docker-demos
cd docker-demos
cmake .
make demo-kip
```

You can now start

```
docker run -it demo-kip
```

You will find this file as `/KIP.MD`.


## Checking your Docker Container

You should find the domain in an environment variable already:

```
shell$ echo $KIP_REALM
unicorn.demo.arpa2.org
```

You can lookup the path to the funny `.lab` host name with:

```
shell$ host -t srv _kip._tcp.$KIP_REALM
_kip._tcp.unicorn.demo.arpa2.org has SRV record 10 10 9876 kipsvc.unicorn.demo.arpa2.lab.
```

You should be able to `ping kipsvc.unicorn.demo.arpa2.lab` and
see it work:

```
shell$ ping -c 4 kipsvc.unicorn.demo.arpa2.lab
PING 193d5e2c77b1 (172.17.0.93) 56(84) bytes of data.
64 bytes from 193d5e2c77b1 (172.17.0.93): icmp_seq=1 ttl=64 time=1.95 ms
64 bytes from 193d5e2c77b1 (172.17.0.93): icmp_seq=2 ttl=64 time=0.132 ms
64 bytes from 193d5e2c77b1 (172.17.0.93): icmp_seq=3 ttl=64 time=0.204 ms
64 bytes from 193d5e2c77b1 (172.17.0.93): icmp_seq=4 ttl=64 time=0.141 ms
```


## Start the KIP Service

To run this demo, first start the KIP Service but **replace the IP address**:

```
kipd 0.0.0.0 9876 /usr/local/src/kip.git/test/bin/unicorn.keytab 1 &
```


## Kipping a Document Up and Down

Now encrypt a document with

```
kip up /var/lib/dpkg/status /tmp/status.kip
```

And decrypt it again with

```
kip down /tmp/status.kip /tmp/status.copy
```

You can see there is no difference with

```
diff /var/lib/dpkg/status /tmp/status.copy
```

## Still Silly

The current demo is minimal, but functionally it gives a good impression.
Work remaining includes:

**ZIP before KIP** or compression before encryption.  This is a good principle
because compaction is useless after encryption, and improves the entropy of the
input, thus making the largest possible search spaces.  This will go into the
`kip up` program.

**Use DER in the file format** because there is a potential of alternative
output for different viewers.  This requires a decent format with extensible
properties.

**Use DER in the protocol** to the KIP Service.  The current protocol is
downright stupid, with a `?` and `!` followed by a message to work on.
This is not extensible, and lacks the following measures.

**Introduce SASL** for authentication of the users.  It is pretty silly to
hand out keys to everyone.

**Introduce an ACL** in each key to limit who may can see them.

**Introduce TLS** to protect both the SASL exchange and the keys in transit.

