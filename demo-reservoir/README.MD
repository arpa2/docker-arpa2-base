# README for Docker Image arpa2:reservoir

> *This is a simple, initial version of the ARPA2 Reservoir
> as designed in the InternetWide.org project, and implemented
> in a variety of ARPA2.net projects.  It should serve as a
> basis for further development and layering.*

This container currently holds:

  * OpenLDAP, exported on port 1388, configured for Reservoir.
  * arpa2shell, the meta-shell for arpa2xxx sub-shells.
  * arpa2reservoir, the sub-shell for resource management.
    **TODO:** The latter does not integrate with `arpa2shell`
    as it does not derive from `arpa2cmd`; it is entirely
    built from scratch.  That may change `;-)`

There are several ARPA2 idea that could be added:

  * WebDAV on port 1761 through [wsgidav](http://wsgidav.readthedocs.io)
  * AMQP 1.0 upload interface for external users
  * SFTP access? for `user@domain.name@host` to a simulated tree
  * LDAP subscription? to (selections of) Resource Collections
  * ATOM retrieval? of (selections of) Resource Collections
  * The SteamWorks Crank to view the repository via JSON
  * A frontend to the SteamWorks Crank
  * Authentication through TLS-KDH, OpenSSH, ...
  * Authorisation of actions via arpa2service
  * An `arpa2acl` shell for ACLs of Resource Collections
  * A SteamWorks Pully Script for ACL subscription
  * An LMDB instance holding subscirbed ACL information
  * Uses of the libarpa2service package

There are many things open for tinkering:

  * Gaining external access to OpenLDAP (and, once built, `wsgidav`)
  * Improving the shells in any way we like
  * Start using the `cmdparser` package in shells


## Deploy the Image

To build this image on top of the `arpa2:base` image:

```
docker build -t rv <THIS-DIRECTORY>
```

The `slapd` is on the main terminal, outputing tons of debugging
information; you can avoid seeing it with the `--detach` option:

```
docker run --detach --network host --hostname reservoir.arpa2 -p 1388:1388 -p 1761:1761 --name rv0 rv
```

You can stop and start it at any time using

```
docker stop rv0
docker start rv0
```

At some point, you will want to forget about the container,

```
docker rm rv0
```

## ARPA2 Shell Access

Shells for poking around can be started as desired:

```
docker exec -ti rv0 arpa2shell
```

This is a special shell for doing ARPA2 manipulations.
In fact, it is a meta-shell that can drop in on various
ARPA2 sub-shells and allows switching between them.
This is more powerful than just opening a single shell,

```
docker exec -ti rv0 arpa2reservoir
```

You can get a normal shell with

```
docker exec -ti rv0 bash
```

If you would to setup GNU readline for more pleasant
editing, you would run this on the shell:

```
arpa2gnu
```

And if you would like to switch to Kerberos authentication
you could use `demo@ARPA2.NET` with password `sekreet`:

```
arpa2kinit
```

To drop Kerberos, instead run

```
arpa2kinit @
```


On the shell, you could also run the shells,

```
arpa2reservoir
arpa2shell
```

Note that the set of domains is independent from those
used in IdentityHub.  They reside in different parts
of the tree, to help with situations where not all
domains have the same service, where subdomains have
additional service, where customers take out only one
but not both the services, and so on.

Once on an `arpa2reservoir` shell, you can do things like
adding domains, Resource Collections underneath domains,
and since both the domain and each Resource Collection
count as a Resource Index, you can use `index add` to
link to a Resource Collection throug its UUID (shown
symbolically below, as it is a random value).  You can
start at a domain's Resource Index with `index domain`
and the traverse locally added names with `index path`.
There may be cycles, such as the `buurman` below that
points from `Smid` to `Bakker` and back again.  The
paths are always finite-sized so you can make any
steps that seem good.

```
domain add orvelte.nep
collection add orvelte.nep Ambachten
collection add orvelte.nep Kunstenaars
collection add orvelte.nep Bakker
collection add orvelte.nep Brood
collection add orvelte.nep Banket
collection add orvelte.nep Smid
collection add orvelte.nep Hoefijzers
collection add orvelte.nep Schilden
collection add orvelte.nep Zwaarden
index domain orvelte.nep
index add {UUID_Kunstenaars} kunst
index add {UUID_Ambachten} ambacht
index path kunst
index add {UUID_Schilden} schilden
index add {UUID_Zwaarden} zwaarden
index add {UUID_Banket} banket
index add {UUID_Bakker} bakker
index add {UUID_Smid} smid
inded domain orvelte.nep
index path ambacht
index add {UUID_Schilden} schilden
index add {UUID_Zwaarden} zwaarden
index add {UUID_Hoefijzers} hoefijzers
index add {UUID_Brood} brood
index add {UUID_Banket} banket
index add {UUID_Bakker} bakker
index add {UUID_Smid} smid
index domain orvelte.nep
index collection {UUID_Smid}
index add {UUID_Schilden} schilden
index add {UUID_Zwaarden} zwaarden
index add {UUID_Hoefijzers} hoefijzers
index add {UUID_Bakker} buurman
index add {UUID_Kunstenaars} kunst
index add {UUID_Ambachten} ambacht
index path buurman
index add {UUID_Brood} brood
index add {UUID_Banket} banket
index add {UUID_Smid} buurman
index add {UUID_Kunstenaars} kunst
index add {UUID_Ambachten} ambacht
index domain orvelte.nep
index path kunst bakker brood
resource add file=/tmp/recept-krentemik.txt type=text/plain name=Recept_Krentemik
```

Make sure to hit `<tab>` often, it should work really
pleasantly.  Use `?command` or `help command` to inquire
about a specific command's syntax.

You can also use the `arpa2acl` shell to set the ACL for
the two kinds of Reservoir Index objects: the client's
domain as represented under the Reservoir root and the
various Reservoir Collections underneath the domain.
Resource are one step further down; these do not have
individual ACL settings but follow Resource Collections.

You can run `slapcat` from another shell to see the
changes in the database.  This command is basically
a dump of the contents of the OpenLDAP database in a
standardised exchange format, LDIF.  This is a rogue
utility, bypassing the protocol and authentication,
so it can only be run locally.

The shells are a bit rudimentary, but they may grow
into management utilities.  By that time we should
probably split the words over the underscore characters,
perhaps using the `cmdparser` package that was installed.


## Using LDAP

The container exports LDAP service over port 389.
It also runs locally on `/tmp/ldap-socket`, reachable with LDAP URI
`ldapi://%2ftmp%2fldap-socket` -- mind the scheme's extra `i` and note
that path separators are escaped to `%2f` to not mix them with URI syntax.

A query that could be made would be

```
ldapsearch -w sekreet -D uid=demo,ou=IdentityHub,o=arpa2.net,ou=InternetWide -b ou=InternetWide labeledURI
```

You should get the `dn` and `labeledURI` for all objects underneath the
base option `-b ou=InternetWide` that are in the database.  The initial data
is loaded from `/root/initial.ldif` as part of the startup script.

This includes the standard `rootdn` and `rootpw` as setup
in `/etc/ldap/slapd.conf` for the server, and for which the `BINDDN` but
not the password is setup in `/etc/ldap/ldap.conf` for the client.


## Image Updates

We currently expect some preparation to building, namely the
addition of `riak_2.2.3-1_amd64.deb` in the current directory.
It is rather big for inclusion in Git, and downloading it is
a bit of a problem given the download infrastructure.

To update this image, please build it with the public tag and
push it:

```
docker tag rv arpa2:reservoir
docker push arpa2:reservoir
```

Cleaning up is easy in docker, but also necessary because of
the dangling images and containers:

```
docker container prune
docker image     prune
```

