# ARPA2 Resource ACL nginx demo

This is a demonstration of the ARPA2 Resource ACL for nginx.

## Create the demo image and run a container
```sh
docker build -t a2aclrnginx .
docker run --add-host 'trucktyres.example:127.0.0.1' -it a2aclrnginx bash
```

```sh
# Start nginx.
# The nginx configuration uses policy file /demopolicy.
/usr/local/nginx/sbin/nginx -c /nginx.conf
crudapp /srv/trucktyres.example &

First we impersonate as Sean, an employee of Fineyear, and try to
put a new tyre in stock that has just rolled out of the factory:
$ curl -v \
    -u sean@fineyear.example: \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '@-' http://trucktyres.example/api/tyres/demotyre <<'EOF'
{
  "serial_number":    "6012021194",
  "service_provider": "Worldmaster",
  "brand":            "Fineyear",
  "size":             "385/65R22.5",
  "type":             "KMAX T"
}
EOF

# Then we try to get the tyre that we just created, which should fail with a 403
# because sean@fineyear.example only has the create permission ("C") and not the
# read permission ("R").
$ curl -u sean@fineyear.example: http://trucktyres.example/api/tyres/demotyre

# Let's retry as brian@worldmaster.example, which does have the "R" permission.
# This should return a 200 with the document.
$ curl -u brian@worldmaster.example: http://trucktyres.example/api/tyres/demotyre
{"serial_number":"6012021194","service_provider":"Worldmaster","brand":"Fineyear","size":"385/65R22.5","type":"KMAX T"}
```

## a2aclmilter usage
a2aclmilter [-dhqv] [-g group] acldb user chrootdir sockaddr

## a2aclmilter manpage
man a2aclmilter

## modify policy for other experiments
vi /demopolicy

[demopolicy]: ./demopolicy
