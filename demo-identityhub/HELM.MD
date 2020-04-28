# Helm -- Fallback/Recovery through Authentication Bootstrapping

> *Using Helm, you can control an online resource "from the outside".
> This may use extremely light-weight identity, even bootstrapping
> your online presence, and be supportive of fallback/recovery by
> you or others.*

Helm lists a number of online resources under a given provider's control.
You login to this provider and see the available resources, with the
option to change them; for instance, add or remove resources or change
their setup.

To this end, we add a number of elements to LDAP directories.

  * `helmOnlineResource` objects can be searched from the Helm to
    learn about objects that might be controlled.
  * `helmType` can be an application-specific type, if the DN and
    `objectClass` are insufficient.
  * `helmCanonical` is a single name for an object that is
    canonical (it would ideally also be unique, but since it may
    be given by you it need not be).
  * `helmIdentity` is matched with an authenticated identity that
    was used to access the Helm.

There can be many kinds of online resources in a Helm:

  * Domain names (administrative access).

  * Individual email addresses and/or phone numbers.

  * Control panel access.

  * ...

A powerful, yet simple approach for deploying a Helm would be:

  * Find a few independent providers of HAAN Service, that is, places
    where you can grab a random identity with corresponding password.
    These sites *do not need to store* this information but can still
    authenticate you when you present the password on later visits.

  * Use an Helm Identity from each of these providers as fallback
    identity on your online resources.  Setting multiple fallback
    identities from independent providers makes you less volnurable
    to problems with one of them.

  * Keep the passwords to yourself.  Preferrably print it and stick
    it in a sealed envelope.  Save different Helm Identities in
    different places.  Consider handing over one of them to another
    person; if it is really important, enclose it into a contract
    and make a lawyer or notary official responsible to execute it
    as you desire.

Each of the Helm Identities can take complete control over the
online resource.  However, since they are never communicated as part
of these resources, they may be changed independently of it, and so
you can modify the control over each online resources as time evolves.
When an employee leaves the company, their control must be retracted,
which is simply done by removing their identity.  Make sure you keep
enough control, though.



