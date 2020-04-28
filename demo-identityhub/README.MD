# README for Docker Image arpa2/identityhub

> *This is a simple, initial version of the IdentityHub
> as designed in the InternetWide.org project, and implemented
> in a variety of ARPA2.net projects.  It should serve as a
> basis for further development and layering.*

This container currently holds:

  * OpenLDAP, exported on port 1389, configured for IdentityHub.
  * web2ldap, a technical web wrapper exported on port 1760.
  * arpa2shell, the meta-shell for arpa2xxx sub-shells.
  * arpa2id, the sub-shell for identity management.

There are several ARPA2 aspects that could be added:

  * The SteamWorks Crank to edit the repository via JSON
  * A frontend to the SteamWorks Crank
  * Automatic creation of Kerberos identities
  * Automatic generation of X.509 and OpenPGP keys
  * Authentication through TLS-KDH, OpenSSH, ...
  * Authorisation of actions via arpa2service
  * An `arpa2acl` shell for ACL editing
  * A SteamWorks Pully Script for ACL subscription
  * An LMDB instance holding subscirbed ACL information
  * Uses of the libarpa2service package

There are many things open for tinkering:

  * Gaining external access to OpenLDAP and web2ldap
  * Improving the shells in any way we like
  * Start using the `cmdparser` package in shells

Once the image runs, you can ask it for the data that was initially
added for user John, using plain OpenLDAP search:

```
shell$ ldapsearch \
	-H ldapi://%2ftmp%2fldap-socket \
	-Y EXTERNAL \
	-b associatedDomain=example.com,ou=IdentityHub,o=arpa2.net,ou=InternetWide
...
# john, example.com, IdentityHub, arpa2.net, InternetWide
dn: uid=john,associatedDomain=example.com,ou=IdentityHub,o=arpa2.net,ou=Intern
 etWide
uid: john
objectClass: inetOrgPerson
objectClass: lifecycleObject
cn: John Doe
sn: Doe
seeAlso: uid=jojo
lifecycleState: humanfate . baby toddler child puber mature senile
```

As you can see, there is an `objectClass: lifecycleObject` and, as permitted by its
schema, a `lifecycleState` attribute (there could be multiple).

We can also zoom in on all those objects under a domain.  This is especially
useful with SyncRepl (perhaps through SteamWorks Pulley) to subscribe to any
new attributes, or old ones being removed.  This is what the LifeCycle backend
is meant for -- to trigger scripts when such changes occur.

```
shell$ ldapsearch \
	-H ldapi://%2ftmp%2fldap-socket \
	-Y EXTERNAL \
	-b associatedDomain=example.com,ou=IdentityHub,o=arpa2.net,ou=InternetWide \
	'(&(objectClass=lifecycleObject)(lifecycleState=*))' \
	lifecycleState
...
# john, example.com, IdentityHub, arpa2.net, InternetWide
dn: uid=john,associatedDomain=example.com,ou=IdentityHub,o=arpa2.net,ou=Intern
 etWide
lifecycleState: humanfate . baby toddler child puber mature senile
```

This is precisely the input expected by the Pulley backend library.  To query
such objects and deliver them to a supportive backend, we might use
PulleyScript like this:

```
# Retrieve from the LDAP root ("world") all the IdentityHub entries
# of lifecycleObject class with at least one lifecycleState attribute
#
ObjectClass:"lifecycleObject" + LifecycleState:lcs, @dn, Uid=user, AssociatedDomain=zone, OU="IdentityHub", O="arpa2.org", OU="InternetWide" <- world

# Filter out only attributes for the humanfate life cycle
#
#MAYNOTWORK# (lifecycleState=humanfate *)

# Deliver those attributes along with their object DN to the
# Pulley backend for lifecycle handling.  Invoke a script to
# handle additions or removals.
#
dn,lcs -> lifecycle (humanfate="/opt/life/bin/humanfate.sh")
```


## Deploy the Image

First, prepare building the `py` subdirectory on a Debian
Stable machine (as that is the target system).  This can
be done by running `Dockerprep.sh` on that machine and
then copying the `py` directory built there in this package
at the same level as the `Dockerprep.sh` file.  We do this
to avoid adding `pip` and its many, many dependencies to
the runtime.

To build this image on top of the `arpa2/base` image:

```
docker build -t idhub <THIS-DIRECTORY>
```

The `slapd` is on the main terminal, outputing tons of debugging
information:

```
docker run --detach --network host --hostname identityhub.arpa2 -p 1389:1389 -p 1760:1760 --name id0 idhub
```

You can stop and start it at any time using

```
docker stop id0
docker start id0
```

At some point, you will want to forget about the container,

```
docker rm id0
```

## ARPA2 Shell Access

Shells for poking around can be started as desired:

```
# Alas, this complains about envvars that are not set
docker exec -ti id0 arpa2shell
```

This is a special shell for doing ARPA2 manipulations.
In fact, it is a meta-shell that can drop in on various
ARPA2 sub-shells and allows switching between them.
This is more powerful than just opening a single shell,

```
# Alas, this complains about envvars that are not set
docker exec -ti id0 arpa2shell
```

You can get a normal shell with

```
docker exec -ti id0 bash
```

On the shell, you could also run the shells,

```
arpa2id
arpa2shell arpa2id # and later more sub-shells
```

Once on an `arpa2id` shell, you can do things like

```
domain_add orvelte.nep Orvelte, Incorporated
user_add orvelte.nep bakker Hij die bakt
user_add orvelte.nep smid Hij die hakt
user_del orvelte.nep bakker
user_del orvelte.nep smid
domain_del orvelte.nep
```

Make sure to hit `<tab>` often, it should work really
pleasantly.  Use `?command` or `help command` to inquire
about a specific command's syntax.

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

The container exports LDAP service over port 1389.
It also runs locally on `/tmp/ldap-socket`, reachable with LDAP URI
`ldapi://%2ftmp%2fldap-socket` -- mind the scheme's extra `i` and note
that path separators are escaped to `%2f` to not mix them with URI syntax.

A query that could be made would be

```
ldapsearch -w sekreet -D uid=admin,ou=IdentityHub,o=arpa2.net,ou=InternetWide -b ou=InternetWide labeledURI
```

You should get the `dn` and `labeledURI` for all objects underneath the
base option `-b ou=InternetWide` that are in the database.  The initial data
is loaded from `/root/initial.ldif` as part of the startup script.

This includes the standard `rootdn` and `rootpw` as setup
in `/etc/ldap/slapd.conf` for the server, and for which the `BINDDN` but
not the password is setup in `/etc/ldap/ldap.conf` for the client.


## Image Updates

The build environment for this image is setup with `virtualenv`.
This allows local installation through `pip`, but take care to
do this on Debian Stable only, to avoid compiling binaries for
another enivironment.  (Maybe we should use a build image too?
The lack of build/run split always confuses me in Docker -Rick)
We would like to move to `pip3` for the `python3` variants, but
`web2ldap` is not at this point yet, and it is our most important
package used.  We think the ARPA2 shells are ready, though.

To update this image, please build it with the public tag and
push it:

```
docker tag idhub arpa2/identityhub
docker push arpa2/identityhub
```

Cleaning up is easy in docker, but also necessary because of
the dangling images and containers:

```
docker container prune
docker image     prune
```

## Future Separation of Build Environment

Apropos [build confusion and small images!](https://docs.docker.com/develop/develop-images/multistage-build/#use-multi-stage-builds) The people over at Docker understood the problem, as one would expect:

  * We can start off building `FROM arpa2/base AS idhub-dev` to collect build image stuff
  * We restart in the same `Dockerfile` with the target, `FROM arpa2/base AS idhub`
  * We can then `COPY --from=idhub-dev /path/in/dev/stage /target/image/location`

A prior phase using `pip` seems the perfect solution then.  It would install a lot of
things but then drop it all, and allow us to copy what we need.  That is *much* better
than the current assumption that you will magically prepare a `py` directory from
another system that you are supposed to setup as an up to date Debian Stable.

