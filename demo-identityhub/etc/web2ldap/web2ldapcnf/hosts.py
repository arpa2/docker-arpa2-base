# -*- coding: utf-8 -*-
"""
web2ldapcnf/hosts.py - Host-related options
(c) by Michael Stroeder <michael@stroeder.com>
"""

from __future__ import absolute_import

# Leave these import lines alone
import os
import ldap0
import certifi

from web2ldap.app.core import etc_dir,templates_dir
import web2ldapcnf
from web2ldap.app.cnf import Web2LDAPConfig

########################################################################
# List of all LDAP hosts to use. These hosts will appear in the
# default select list of the login form.
# A list containing only one host results in a normal input field
# with the host set as default.
########################################################################

ldap_uri_list = [
  'ldap://localhost',
  (
    'ldap://localhost:389/ou=IdentityHub,o%3Dinternetwide.org,ou%3DARPA2',
    u'IdentityHub server over LDAP to localhost:389'
  ),
  (
    'ldapi://%2Ftmp%2Fldap-socket',
    u'OpenLDAP server with IdentityHub over UNIX domain socket'
  ),
  ('ldaps://demo.ae-dir.com/ou=ae-dir????bindname=uid%3Daead%2Cou%3Dae-dir,X-BINDPW=CorrectHorseBatteryStaple',u'Æ-DIR demo role Æ admin'),
  ('ldap://ipa.demo1.freeipa.org/dc=demo1,dc=freeipa,dc=org??one??bindname=uid%3Dadmin%2Ccn%3Dusers%2Ccn%3Daccounts%2Cdc%3Ddemo1%2Cdc%3Dfreeipa%2Cdc%3Dorg,X-BINDPW=Secret123','freeIPA demo as admin'),
  ('ldap://db.debian.org/dc=debian,dc=org??one',u'debian.org Developers LDAP Search'),
  ('ldap://x500.bund.de/o=Bund,c=DE??one',u'X.500 Directory Informationsverbund Berlin-Bonn'),
  ('ldap://pks-ldap.telesec.de/c=DE',u'T-TeleSec PKS'),
  ('ldap://ldap.nrca-ds.de/dc=ldap,dc=nrca-ds,dc=de??one',u"Qualified certificates of german BNetzA"),
  'ldap://ldap.itd.umich.edu',
  ('ldap://ldap.swissdigicert.ch/dc%3Dswissdigicert%2Cdc%3Dch??one?',u'SwissDigiCert'),
  ('ldap://ldap.a-trust.at/c=AT??one?',u'A-Trust PKI Verzeichnisdienst'),
  ('ldap://directory.s-trust.de',u'S-Trust'),
  ('ldap://ldap1.pca.dfn.de/ou%3DDFN-PKI%2Co%3DDFN-Verein%2Cc%3Dde??one',u'DFN-PKI'),
  ('ldap://ldap.sbca.telesec.de/c=de??one',u'T-Systems Shared Business'),
  ('ldap://ldap.crl.esecure.datev.de/??one',u'Datev'),
  ('ldap://directory.swisssign.net/o=SwissSign,c=CH??one',u'SwissSign AG'),
  ('ldap://ldap.forumsys.com/dc=example,dc=com????bindname=cn%3Dread-only-admin%2Cdc%3Dexample%2Cdc%3Dcom,X-BINDPW=password',u'ldap.forumsys.com'),
]

# Set to True (or 1) if LDAP access should be restricted to the LDAP servers
# defined in ldap_uri_list (default if absent is 0 - restriction disabled)
restricted_ldap_uri_list = 0

########################################################################
# Init some re-usable preset configuration instances
# which are registered in ldap_def below
########################################################################

#---------------------------------------------------------------------------
# Presets for MS Active Directory
#---------------------------------------------------------------------------

msad_config = Web2LDAPConfig(
  description=u'MS Active Directory',
  searchform_template= {
    u'_':os.path.join(templates_dir,'searchform_msad.html'),
  },
  requested_attrs=[
    'structuralObjectClass','subschemaSubentry',
    # counters
    'hasSubordinates',
    # Dynamic Entries (see RFC 2589)
    'entryTTL',
    # MS Active Directory
    'nTSecurityDescriptor',
    'tokenGroups','tokenGroupsGlobalAndUniversal','tokenGroupsNoGCAcceptable',
    'mS-DS-CreatorSID','primaryGroupToken','canonicalName','fromEntry',
    'sDRightsEffective','msDS-Approx-Immed-Subordinates','msDS-KeyVersionNumber',
    'msDS-ReplAttributeMetaData',
    'lastLogonTimestamp','lockoutTime',
    'allowedAttributes','allowedAttributesEffective','allowedChildClasses','allowedChildClassesEffective',
  ],
  modify_constant_attrs=[
    'uSNChanged','uSNCreated','whenChanged','whenCreated',
  ],
)

#---------------------------------------------------------------------------
# Presets for OpenLDAP's accesslog DB
#---------------------------------------------------------------------------

openldap_accesslog_config = Web2LDAPConfig(
  description=u'OpenLDAP accesslog',
  search_tdtemplate= {
    'auditSearch':r"""<strong>%(reqType)s</strong> %(reqStart)s session %(reqSession)s<br>
                      &rArr; %(reqResult)s: %(reqMessage)s<br>Search %(reqScope)s: %(reqDN)s<br>%(reqFilter)s""",
    'auditBind':r"""<strong>%(reqType)s</strong> %(reqStart)s session %(reqSession)s<br>
                      &rArr; %(reqResult)s: %(reqMessage)s: %(reqSession)s<br>%(reqDN)s""",
    'auditAdd':r"""<strong>%(reqType)s</strong> %(reqStart)s session %(reqSession)s<br>
                      &rArr; %(reqResult)s: %(reqMessage)s<br>Entry %(reqDN)s added<br>by %(reqAuthzID)s""",
    'auditModify':r"""<strong>%(reqType)s</strong> %(reqStart)s session %(reqSession)s<br>
                      &rArr; %(reqResult)s: %(reqMessage)s<br>Entry %(reqDN)s modified<br>by %(reqAuthzID)s""",
    'auditModRDN':r"""<strong>%(reqType)s</strong> %(reqStart)s session %(reqSession)s<br>
                      &rArr; %(reqResult)s: %(reqMessage)s<br>Entry %(reqDN)s renamed to %(reqNewRDN)s,%(reqNewSuperior)s<br>by %(reqAuthzID)s""",
    'auditObject':r"""<strong>%(reqType)s</strong> %(reqStart)s session %(reqSession)s<br>
                      &rArr; %(reqResult)s: %(reqMessage)s<br>by %(reqAuthzID)s""",
    'auditDelete':r"""<strong>%(reqType)s</strong> %(reqStart)s session %(reqSession)s<br>
                      &rArr; %(reqResult)s: %(reqMessage)s<br>Entry %(reqDN)s deleted<br>by %(reqAuthzID)s""",
    'auditAbandon':r"""<strong>%(reqType)s</strong> %(reqStart)s session %(reqSession)s<br>
                      &rArr; %(reqResult)s: %(reqMessage)s<br>Abandonded %(reqId)s by %(reqAuthzID)s""",
  },
  searchform_template= {
    u'_':os.path.join(templates_dir,'searchform_accesslog.html'),
  },
  search_attrs=[
    'objectClass',
    'reqAuthzID','reqDN','reqEnd','reqEntryUUID','reqMod','reqOld',
    'reqResult','reqSession','reqStart','reqType',
  ],
  read_template={
    'auditAdd':os.path.join(templates_dir,'openldap','read_auditAdd.html'),
    'auditModify':os.path.join(templates_dir,'openldap','read_auditAdd.html'),
    'auditModRDN':os.path.join(templates_dir,'openldap','read_auditModRDN.html'),
    'auditDelete':os.path.join(templates_dir,'openldap','read_auditDelete.html'),
  },
)

#---------------------------------------------------------------------------
# Presets for changelog database
#---------------------------------------------------------------------------

changelog_config = Web2LDAPConfig(
  description=u'changelog',
  search_tdtemplate= {
    'changelogentry':r'No. %(changenumber)s at %(changetime)s<br>%(changetype)s %(targetdn)s (%(targetentryuuid)s)<br>by %(changeInitiatorsName)s',
  },
  searchform_template= {
    u'_':os.path.join(templates_dir,'searchform_changelog.html'),
  },
  search_attrs=[
    'changeType','targetDN','targetEntryUUID','changeTime',
    'changeLogCookie','replicaIdentifier','replicationCSN','changeInitiatorsName',
  ],
  read_template={
    'changeLogEntry':os.path.join(templates_dir,'read_changeLogEntry.html'),
  },
)

#---------------------------------------------------------------------------
# Presets for OpenLDAP's cn=monitor
#---------------------------------------------------------------------------

openldap_monitor_config = Web2LDAPConfig(
  # Important workaround for OpenLDAP bug ITS#7053 !!!
  search_resultsperpage=0,
  search_tdtemplate= {
    # for OpenLDAP
    'monitorOperation':r'%(cn)s operations: %(monitorOpCompleted)s of %(monitorOpInitiated)s completed',
    'monitoredObject':r"""%(cn)s: %(monitoredInfo)s<br>
       %(monitorTimestamp)s %(namingContexts)s %(labeledURI)s<br>
       %(seeAlso)s
      """,
    'monitorContainer':r'%(cn)s - %(description)s',
    'monitorCounterObject':r'%(cn)s: %(monitorCounter)s',
    'monitorConnection':r"""Connection %(monitorConnectionNumber)s (LDAPv%(monitorConnectionProtocol)s):<br>
      %(monitorConnectionPeerAddress)s &raquo; %(monitorConnectionListener)s<br>
      %(monitorConnectionAuthzDN)s<br>
      (ops r: %(monitorConnectionOpsReceived)s, e: %(monitorConnectionOpsExecuting)s, p: %(monitorConnectionOpsPending)s, c: %(monitorConnectionOpsCompleted)s)
      """,
  },
  read_template={
    # for OpenLDAP
    'monitorConnection':os.path.join(templates_dir,'read_monitorConnection.html'),
  },
)

#---------------------------------------------------------------------------
# Presets for cn=config supporting various vendors
#---------------------------------------------------------------------------

# For dynamic configuration via cn=config
cn_config = Web2LDAPConfig(
  description=u"Configuration backend",
  search_tdtemplate={
    # for OpenLDAP
    'olcModuleList':r'Modules from %(olcModulePath)s',
    'olcDatabaseConfig':r'Database <em>%(olcDatabase)s</em> suffix %(olcSuffix)s',
    'olcSchemaConfig':r'Schema <em>%(cn)s</em>',
    'olcOverlayConfig':r'Overlay <em>%(olcOverlay)s</em>',
    # for OpenDS/OpenDJ
    'ds-cfg-backend':r'Backend <em>%(ds-cfg-backend-id)s</em>, suffix <em>%(ds-cfg-base-dn)s</em><br>Class: %(ds-cfg-java-class)s',
    'ds-cfg-local-db-index':r'Index for <em>%(ds-cfg-attribute)s</em>: <em>%(ds-cfg-index-type)s</em>',
    'ds-cfg-replication-server':r"""
      Replication server-id <em>%(ds-cfg-replication-server-id)s</em>:<br>
      Replication server(s): %(ds-cfg-replication-server)s
    """,
    'ds-cfg-replication-domain':r"""
      Replication domain <em>%(cn)s</em>:<br>
      Server-ID: %(ds-cfg-server-id)s<br>
      Base-DN: %(ds-cfg-base-dn)s<br>
      Replication server(s): %(ds-cfg-replication-server)s
    """,
  },
  read_template={
    # for OpenLDAP
    'olcGlobal':os.path.join(templates_dir,'openldap','read_olcGlobal.html'),
    'olcHdbConfig':os.path.join(templates_dir,'openldap','read_olcHdbConfig.html'),
    'olcMdbConfig':os.path.join(templates_dir,'openldap','read_olcMdbConfig.html'),
  },
  input_template={
    # for OpenLDAP
    'olcGlobal':os.path.join(templates_dir,'openldap','inputform_olcGlobal.html'),
    'olcHdbConfig':os.path.join(templates_dir,'openldap','inputform_olcHdbConfig.html'),
    'olcMdbConfig':os.path.join(templates_dir,'openldap','inputform_olcMdbConfig.html'),
  },
  # HTML template strings used to display the superior entry
  # in the input form when adding/modifying entries
  inputform_supentrytemplate={
    # for OpenLDAP
    'olcDatabaseConfig':r"""<table>
        <tr><td>Database name:</td><td>%(olcDatabase)s</td></tr>
        <tr><td>Suffix:</td><td>%(olcSuffix)s</td></tr>
      </table>
    """,
  },
  addform_entry_templates={
    # for OpenLDAP
    u'Modules':os.path.join(templates_dir,'openldap','add_olcModuleList.ldif'),
    u'Database - Adress book (back-hdb)':os.path.join(templates_dir,'openldap','add_olcHdbConfig_AddressBook.ldif'),
    u'Database - Unix Users (back-hdb)':os.path.join(templates_dir,'openldap','add_olcHdbConfig_UnixUsers.ldif'),
    u'Database - Accesslog (back-hdb)':os.path.join(templates_dir,'openldap','add_olcHdbConfig_accesslog.ldif'),
    u'Database - LDAP-Proxy (back-ldap)':os.path.join(templates_dir,'openldap','add_olcLdapConfig.ldif'),
    u'Database - back-mdb':os.path.join(templates_dir,'openldap','add_olcMdbConfig.ldif'),
    u'Overlay - Syncrepl-Provider (slapo-syncprov)':os.path.join(templates_dir,'openldap','add_olcHdbConfig_accesslog.ldif'),
    u'Overlay - Accesslog (slapo-accesslog)':os.path.join(templates_dir,'openldap','add_olcHdbConfig_accesslog.ldif'),
    u'Overlay - Accesslog (slapo-accesslog)':os.path.join(templates_dir,'openldap','add_olcHdbConfig_accesslog.ldif'),
    u'Schema config':os.path.join(templates_dir,'openldap','add_olcSchemaConfig.ldif'),
  },
)

#---------------------------------------------------------------------------
# Presets for Æ-DIR
#---------------------------------------------------------------------------

ae_dir_config = Web2LDAPConfig(
  description=u'Æ-DIR',
  top_template= os.path.join(templates_dir,'ae-dir','top.html'),
  binddnsearch=ur'(|(uid=%s)(uidNumber=%s))',
  boundas_template= {
    'aeUser':r'<span title="%(displayName)s: %(description)s">%(uid)s: %(description)s</span>',
  },
  session_track_control=1,
  supplement_schema=os.path.join(etc_dir,'ae-suppl-schema.ldif'),
  modify_constant_attrs=[
    # Mostly OpenLDAP
    'entryCSN','entryDN','entryUUID',
    # see RFC
    'createTimestamp','modifyTimestamp','creatorsName','modifiersName',
  ],
  login_template=os.path.join(templates_dir,'ae-dir','login.html'),
  addform_parent_attrs=['entryUUID'],
  search_attrs=[
    'aeDept',
    'aeDevicePort',
    'aeDeviceSlot',
    'aeDisplayNameGroups',
    'aeFqdn',
    'aeHost',
    'aeHwSerialNumber',
    'aeLocation',
    'aeLoginGroups',
    'aeLogStoreGroups',
    'aeLogStorePeriod',
    'aeNotAfter',
    'aeNotBefore',
    'aeNwDevice',
    'aePasswordAdmins',
    'aePerson',
    'aeProxyFor',
    'aeRemoteHost',
    'aeSetupGroups',
    'aeSourceUri',
    'aeSrvGroup',
    'aeStatus',
    'aeStockId',
    'aeTag',
    'aeTicketId',
    'aeVisibleGroups',
    'aeVisibleSudoers',
    'aeZoneAdmins',
    'aeZoneAuditors'
    'authTimestamp',
    'cn',
    'createTimestamp',
    'creatorsName',
    'departmentNumber',
    'description',
    'displayName',
    'distinguishedName',
    'employeeNumber',
    'employeeType',
    'entryDN',
    'entryUUID',
    'facsimileTelephoneNumber',
    'gidNumber',
    'givenName',
    'hasSubordinates',
    'homeDirectory',
    'homePhone',
    'host',
    'ipHostNumber',
    'ipNetmaskNumber',
    'ipNetworkNumber',
    'l',
    'labeledURI',
    'loginShell',
    'macAddress',
    'mail',
    'manager',
    'member',
    'memberOf',
    'memberURL',
    'mobile',
    'modifiersName',
    'modifyTimestamp',
    'msPwdResetAdminPw',
    'msPwdResetEnabled',
    'msPwdResetExpirationTime',
    'msPwdResetPasswordHash',
    'msPwdResetTimestamp',
    'name',
    'o',
    'oathFailureCount',
    'oathHMACAlgorithm',
    'oathHOTPCounter',
    'oathHOTPParams',
    'oathHOTPToken',
    'oathLastFailure',
    'oathLastLogin',
    'oathSecretTime',
    'oathThrottleLimit',
    'oathToken',
    'oathTokenIdentifier',
    'oathTokenSerialNumber',
    'oathTOTPParams',
    'oathTOTPToken',
    'objectClass',
    'ou',
    'personalTitle',
    'postalAddress',
    'postalCode',
    'pwdAccountLockedTime',
    'pwdAllowUserChange',
    'pwdAttribute',
    'pwdChangedTime',
    'pwdFailureTime',
    'pwdHistory',
    'pwdLockout',
    'pwdMustChange',
    'pwdPolicySubentry',
    'pwdReset',
    'seeAlso',
    'serialNumber',
    'sn',
    'sshPublicKey',
    'street',
    'structuralObjectClass',
    'sudoCommand',
    'sudoHost',
    'sudoNotAfter',
    'sudoNotBefore',
    'sudoOption',
    'sudoOrder',
    'sudoRunAs',
    'sudoRunAsGroup',
    'sudoRunAsUser',
    'sudoUser',
    'telephoneNumber',
    'title',
    'uid',
    'uidNumber',
    'uniqueIdentifier',
    'userPassword',
  ],
  searchform_search_root_url='ldap:///ou=ae-dir??one?(|(objectClass=aeZone))',
  searchform_template= {
    u'_':os.path.join(templates_dir,'ae-dir','searchform_aedir.html'),
  },
  search_tdtemplate= {
    'aeUser':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      %(displayName)s / %(description)s<br>
      <dl>
        <dt>Member of:</dt>
        <dd>%(memberOf)s</dd>
      </dl>
    </div>
    """,
    'aeDept':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      %(ou)s (%(departmentNumber)s)
    </div>
    """,
    'aePerson':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      %(displayName)s &lt;%(mail)s&gt;
    </div>
    """,
    'aeGroup':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      User group %(cn)s (%(gidNumber)s):<br>
      %(description)s
    </div>
    """,
    'aeMailGroup':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Mail group %(cn)s &lt;%(mail)s&gt;<br>
      %(description)s
    </div>
    """,
    'aeSrvGroup':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Server group %(cn)s:<br>
      %(description)s
    </div>
    """,
    'aeService':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Service account %(uid)s:<br>
      %(description)s
      <dl>
        <dt>Member of:</dt>
        <dd>%(memberOf)s</dd>
      </dl>
    </div>
    """,
    'aeHost':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Server %(cn)s: %(host)s<br>
      %(description)s
    </div>
    """,
    'aeNwDevice':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      %(aeFqdn)s:<br>
      inet addr:%(ipHostNumber)s<br>
      HWaddr: %(macAddress)s
    </div>
    """,
    'aeSudoRule':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Sudo rule %(cn)s:<br>
      %(description)s
    </div>
    """,
    'aeTag':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Tag %(cn)s: %(description)s
    </div>
    """,
    'aeZone':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Zone %(cn)s: %(description)s
    </div>
    """,
    'aeRoot':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Org unit %(ou)s:<br>
      %(description)s
    </div>
    """,
    'aeAuthcToken':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Authentication token %(displayName)s
    </div>
    """,
    'aePolicy':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Policy %(cn)s: %(description)s
    </div>
    """,
    'aeContact':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Contact %(cn)s: %(description)s
      <dl>
        <dt>Member of:</dt>
        <dd>%(memberOf)s</dd>
      </dl>
    </div>
    """,
    'aeLocation':r"""
    <div class="aestatus%(aeStatus)s">
      <var>%(entryDN)s</var><br>
      Location %(displayName)s
    </div>
    """,
  },
  read_template={
    'msPwdResetObject':os.path.join(templates_dir,'ae-dir','read_msPwdResetObject.html'),
    'posixAccount':os.path.join(templates_dir,'read_posixAccount.html'),
    'aePolicy':os.path.join(templates_dir,'ae-dir','read_aePolicy.html'),
    'pwdPolicy':os.path.join(templates_dir,'read_pwdPolicy.html'),
    'msPwdResetPolicy':os.path.join(templates_dir,'read_msPwdResetPolicy.html'),
    'aeRoot':os.path.join(templates_dir,'ae-dir','read_aeRoot.html'),
    'aeGroup':os.path.join(templates_dir,'ae-dir','read_aeGroup.html'),
    'aeMailGroup':os.path.join(templates_dir,'ae-dir','read_aeMailGroup.html'),
    'aeDept':os.path.join(templates_dir,'ae-dir','read_aeDept.html'),
    'aeLocation':os.path.join(templates_dir,'ae-dir','read_aeLocation.html'),
    'aePerson':os.path.join(templates_dir,'ae-dir','read_aePerson.html'),
    'aeHost':os.path.join(templates_dir,'ae-dir','read_aeHost.html'),
    'aeService':os.path.join(templates_dir,'ae-dir','read_aeService.html'),
    'aeSrvGroup':os.path.join(templates_dir,'ae-dir','read_aeSrvGroup.html'),
    'aeSudoRule':os.path.join(templates_dir,'ae-dir','read_aeSudoRule.html'),
    'aeTag':os.path.join(templates_dir,'ae-dir','read_aeTag.html'),
    'aeUser':os.path.join(templates_dir,'ae-dir','read_aeUser.html'),
    'aeAuthcToken':os.path.join(templates_dir,'ae-dir','read_aeAuthcToken.html'),
    'aeZone':os.path.join(templates_dir,'ae-dir','read_aeZone.html'),
    'aePerson':os.path.join(templates_dir,'ae-dir','read_aePerson.html'),
    'aeContact':os.path.join(templates_dir,'ae-dir','read_aeContact.html'),
    'aePosixIdRanges':os.path.join(templates_dir,'ae-dir','read_aePosixIdRanges.html'),
    'mailboxRelatedObject':os.path.join(templates_dir,'read_mailboxRelatedObject.html'),
    'namedObject':os.path.join(templates_dir,'read_namedObject.html'),
    'namedPolicy':os.path.join(templates_dir,'read_namedPolicy.html'),
    'inetLocalMailRecipient':os.path.join(templates_dir,'read_inetLocalMailRecipient.html'),
    'oathHOTPUser':os.path.join(templates_dir,'oath','read_oathHOTPUser.html'),
    'oathTOTPUser':os.path.join(templates_dir,'oath','read_oathTOTPUser.html'),
    'oathHOTPToken':os.path.join(templates_dir,'oath','read_oathHOTPToken.html'),
    'oathTOTPToken':os.path.join(templates_dir,'oath','read_oathTOTPToken.html'),
    'oathParams':os.path.join(templates_dir,'oath','read_oathParams.html'),
    'oathHOTPParams':os.path.join(templates_dir,'oath','read_oathHOTPParams.html'),
    'oathTOTPParams':os.path.join(templates_dir,'oath','read_oathTOTPParams.html'),
  },
  input_template={
    'msPwdResetObject':os.path.join(templates_dir,'ae-dir','inputform_msPwdResetObject.html'),
    'posixAccount':os.path.join(templates_dir,'inputform_posixAccount.html'),
    'aePolicy':os.path.join(templates_dir,'ae-dir','inputform_aePolicy.html'),
    'pwdPolicy':os.path.join(templates_dir,'inputform_pwdPolicy.html'),
    'msPwdResetPolicy':os.path.join(templates_dir,'inputform_msPwdResetPolicy.html'),
    'aeDept':os.path.join(templates_dir,'ae-dir','inputform_aeDept.html'),
    'aeLocation':os.path.join(templates_dir,'ae-dir','inputform_aeLocation.html'),
    'aeGroup':os.path.join(templates_dir,'ae-dir','inputform_aeGroup.html'),
    'aeMailGroup':os.path.join(templates_dir,'ae-dir','inputform_aeMailGroup.html'),
    'aeHost':os.path.join(templates_dir,'ae-dir','inputform_aeHost.html'),
    'aeService':os.path.join(templates_dir,'ae-dir','inputform_aeService.html'),
    'aeSrvGroup':os.path.join(templates_dir,'ae-dir','inputform_aeSrvGroup.html'),
    'aeSudoRule':os.path.join(templates_dir,'ae-dir','inputform_aeSudoRule.html'),
    'aeTag':os.path.join(templates_dir,'ae-dir','inputform_aeTag.html'),
    'aeUser':os.path.join(templates_dir,'ae-dir','inputform_aeUser.html'),
    'aeAuthcToken':os.path.join(templates_dir,'ae-dir','inputform_aeAuthcToken.html'),
    'aeZone':os.path.join(templates_dir,'ae-dir','inputform_aeZone.html'),
    'aePerson':os.path.join(templates_dir,'ae-dir','inputform_aePerson.html'),
    'aeContact':os.path.join(templates_dir,'ae-dir','inputform_aeContact.html'),
    'aePosixIdRanges':os.path.join(templates_dir,'ae-dir','inputform_aePosixIdRanges.html'),
    'mailboxRelatedObject':os.path.join(templates_dir,'inputform_mailboxRelatedObject.html'),
    'namedObject':os.path.join(templates_dir,'inputform_namedObject.html'),
    'namedPolicy':os.path.join(templates_dir,'inputform_namedPolicy.html'),
    'inetLocalMailRecipient':os.path.join(templates_dir,'inputform_inetLocalMailRecipient.html'),
    'oathHOTPUser':os.path.join(templates_dir,'oath','inputform_oathHOTPUser.html'),
    'oathTOTPUser':os.path.join(templates_dir,'oath','inputform_oathTOTPUser.html'),
    'oathHOTPToken':os.path.join(templates_dir,'oath','inputform_oathHOTPToken.html'),
    'oathTOTPToken':os.path.join(templates_dir,'oath','inputform_oathTOTPToken.html'),
    'oathParams':os.path.join(templates_dir,'oath','inputform_oathParams.html'),
    'oathHOTPParams':os.path.join(templates_dir,'oath','inputform_oathHOTPParams.html'),
    'oathTOTPParams':os.path.join(templates_dir,'oath','inputform_oathTOTPParams.html'),
  },
  inputform_supentrytemplate={
    'aeRoot':r'<em>%(entryDN)s</em><br>%(description)s (aeRoot)',
    'aeZone':r'<em>%(entryDN)s</em><br>Zone <strong>%(cn)s</strong>: <br>%(description)s',
    'aeSrvGroup':r'<em>%(entryDN)s</em><br>Server/service group <strong>%(cn)s</strong>: <br>%(description)s',
    'aeHost':r'<em>%(entryDN)s</em><br>Host/server <strong>%(host)s</strong>: <br>%(description)s',
  },
  addform_entry_templates={
    u'Æ-DIR tag':os.path.join(templates_dir,'ae-dir','add_aeTag.ldif'),
    u'Æ-DIR user group':os.path.join(templates_dir,'ae-dir','add_aeGroup.ldif'),
    u'Æ-DIR mail group':os.path.join(templates_dir,'ae-dir','add_aeMailGroup.ldif'),
    u'Æ-DIR primary user account':os.path.join(templates_dir,'ae-dir','add_aeUser_inetLocalMailRecipient.ldif'),
    u'Æ-DIR personal user account':os.path.join(templates_dir,'ae-dir','add_aeUser.ldif'),
    u'Æ-DIR OATH-HOTP token':os.path.join(templates_dir,'ae-dir','add_oath_hotp_token.ldif'),
#    u'Æ-DIR OATH-TOTP token':os.path.join(templates_dir,'ae-dir','add_oath_totp_token.ldif'),
    u'Æ-DIR password policy':os.path.join(templates_dir,'ae-dir','add_pwdPolicy.ldif'),
    u'Æ-DIR OATH-HOTP parameters':os.path.join(templates_dir,'ae-dir','add_oathHOTPParams.ldif'),
    u'Æ-DIR person':os.path.join(templates_dir,'ae-dir','add_aePerson.ldif'),
    u'Æ-DIR contact':os.path.join(templates_dir,'ae-dir','add_aeContact.ldif'),
    u'Æ-DIR department':os.path.join(templates_dir,'ae-dir','add_aeDept.ldif'),
    u'Æ-DIR location':os.path.join(templates_dir,'ae-dir','add_aeLocation.ldif'),
    u'Æ-DIR network device':os.path.join(templates_dir,'ae-dir','add_aeNwDevice.ldif'),
    u'Æ-DIR server/service group':os.path.join(templates_dir,'ae-dir','add_aeSrvGroup.ldif'),
    u'Æ-DIR server/host':os.path.join(templates_dir,'ae-dir','add_aeHost.ldif'),
    u'Æ-DIR service/tool account':os.path.join(templates_dir,'ae-dir','add_aeService.ldif'),
    u'Æ-DIR zone':os.path.join(templates_dir,'ae-dir','add_aeZone.ldif'),
    u'Æ-DIR zone admins group':os.path.join(templates_dir,'ae-dir','add_aeGroup_zone-admins.ldif'),
    u'Æ-DIR zone auditors group':os.path.join(templates_dir,'ae-dir','add_aeGroup_zone-auditors.ldif'),
    u'Æ-DIR replica account':os.path.join(templates_dir,'ae-dir','add_slapd-replica.ldif'),
    u'Æ-DIR login proxy':os.path.join(templates_dir,'ae-dir','add_login-proxy.ldif'),
    u'Æ-DIR sudo su - root':os.path.join(templates_dir,'ae-dir','add_aeSudoRule_su_root.ldif'),
  },
  passwd_template= os.path.join(templates_dir,'ae-dir','passwd.html'),
  passwd_hashtypes=['ssha',''],
  passwd_genchars=ur'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
  passwd_genlength=24,
  groupadm_filterstr_template=r'(&(|(objectClass=aeGroup)(objectClass=aeMailGroup))(aeStatus=0)(!(memberURL=*))(|%s))',
  groupadm_optgroup_bounds=(-2,-1),
  groupadm_defs={
    'groupOfEntries':('member',None,True),
    'posixGroup':('memberUid','uid',False),
    'nisMailAlias':('rfc822MailMember','mail',False),
  },
  read_tablemaxcount={
    'member':40,
    'memberUid':40,
    'memberOf':30,
  },
  requested_attrs=[
    # Proxy Authz attributes
    'authzTo','authzFrom',
    # password policy attributes
    'pwdPolicySubentry',
  ],
  rename_supsearchurl={
    u'Search for zone (aeZone)':'ldap:///_??one?(objectClass=aeZone)',
    u'Search for server/service group (aeSrvGroup)':'ldap:///_??sub?(objectClass=aeSrvGroup)',
  },
  # Use delold: 1 with MODRDN requests when doing bulk renaming
  bulkmod_delold=1,
)

########################################################################
# LDAP host(s) with their defaults can be pre-defined as dictionary
# ldap_def = {'host:port':{paramdictionary}}
# You can use preset configuration instance declared above herein
########################################################################

ldap_def = {

  # Overall default values.
  # There's most times no need to adjust the values in this section
  # since they can be overridden by host specific sections (see below).
  '_': Web2LDAPConfig(

    # Search filter template for smart login
    # Use indexed attributes here!
    binddnsearch=ur'(|(cn=%s)(uid=%s)(sAMAccountName=%s)(userPrincipalName=%s))',

    # HTML template strings used to bind name in the status section
    # on top of page depending on the object class of an entry.
    boundas_template= {
      'inetOrgPerson':r'<strong>%(cn)s</strong> &lt;%(mail)s&gt; (%(uid)s/%(employeeNumber)s)',
      'account':r'<strong>%(uid)s</strong>',
    },

    # Timeout for LDAP operations (seconds)
    timeout=300,

    # Use StartTLS on connect. It's recommended saying 0 as default
    # since not many servers can handle an unknown extended operation properly
    starttls=0,

    # Dictionary for specifying arbitrary TLS-related LDAP options.
    # Which options are really available on your system depends on your ldap0 and OpenLDAP builds.
    # (see section TLS OPTIONS on OpenLDAP's man page ldap_set_option(3)
    tls_options={
      # you should really set this!
      ldap0.OPT_X_TLS_REQUIRE_CERT:ldap0.OPT_X_TLS_DEMAND,
      # Directory containing all the trusted root CA certs (symbolic hash links required!)
#      LDAP_OPT_X_TLS_CACERTDIR = os.path.sep.join(etc_dir,'ssl','crt'),
      # File containing all the trusted root CA certs
#      ldap0.OPT_X_TLS_CACERTFILE:os.path.join(etc_dir,'ssl','crt','trusted-certs.crt'),
      ldap0.OPT_X_TLS_CACERTFILE:certifi.where(),
#      ldap0.OPT_X_TLS_CIPHER_SUITE:'ECDHE-RSA-AES256-SHA:DHE-RSA-AES256-SHA',
      ldap0.OPT_X_TLS_PROTOCOL_MIN:3,
#      ldap0.OPT_X_TLS_CRLCHECK:ldap0.OPT_X_TLS_CRL_PEER,
#      ldap0.OPT_X_TLS_CRLFILE:os.path.join(etc_dir,'ssl','crt','peers.crl'),
    },

    # Send session track control
    session_track_control=0,

    # Attributes explicitly requested while doing read
    # and modify operations
    requested_attrs=[
      'structuralObjectClass','governingStructureRule','subschemaSubentry',
      # password policy attributes
      'passwordExpirationTime','passwordExpWarned',
      'passwordRetryCount','retryCountResetTime','accountUnlockTime',
      'passwordHistory','passwordAllowChangeTime',
      # Account specifics
      'nsAccountLock','nsLookthroughLimit',
      # ACL attributes
      'aci','aclentry',
      # counters
      'hasSubordinates','numSubordinates','subordinateCount',
      # Dynamic Entries (see RFC 2589)
      'entryTTL',
      # Proxy Authz attributes
      'authzTo','authzFrom',
      # password policy attributes
      'pwdPolicySubentry',
      # Sun Directory Server
      'isMemberOf',
      # MS Active Directory
      'nTSecurityDescriptor',
      'tokenGroups','tokenGroupsGlobalAndUniversal','tokenGroupsNoGCAcceptable',
      'mS-DS-CreatorSID','primaryGroupToken','canonicalName','fromEntry',
      'sDRightsEffective','msDS-Approx-Immed-Subordinates','msDS-KeyVersionNumber',
#      'msDS-ReplAttributeMetaData',
#      'lastLogonTimestamp','lockoutTime',
#      'allowedAttributes','allowedAttributesEffective','allowedChildClasses','allowedChildClassesEffective',
      # X.500 DSAs
      'administrativeRole',
    ],

    # List of attribute type names which are supposed to be constant during
    # editing an entry.
    modify_constant_attrs=[
      # Mostly OpenLDAP
      'entryCSN','entryDN','entryUUID',
      # see RFC
      'createTimestamp','modifyTimestamp','creatorsName','modifiersName',
      # MS AD
      'uSNChanged','uSNCreated','whenChanged','whenCreated',
      # Netscape/Sun DS
      'nsUniqueId',
      # 389 Directory Server also known as Fedora DS
      'entryUSN',
      # eDirectory
      'localEntryID','GUID',
    ],

    # vCard template files
    vcard_template={
      # 'object class':'pathname of vCard template file'
      'person':os.path.join(templates_dir,'vcard_person.txt'),
      'inetOrgPerson':os.path.join(templates_dir,'vcard_person.txt'),
      'organization':os.path.join(templates_dir,'vcard_organization.txt'),
    },

    # HTML template files for printing table entries
    print_template={
      # 'object class':'pathname of printable HTML template file'
      'person':os.path.join(templates_dir,'print_person.html'),
      'organization':os.path.join(templates_dir,'print_organization.html'),
      'organizationalUnit':os.path.join(templates_dir,'print_organizationalUnit.html'),
    },

    # HTML template file for search options fieldset in search forms
    searchoptions_template=os.path.join(templates_dir,'searchform_search_options.html'),

    # HTML template file for Basic Search form
    searchform_template= {
      u'_':os.path.join(templates_dir,'searchform_base.html'),
      u'NIS':os.path.join(templates_dir,'searchform_nis.html'),
      u'DHCP':os.path.join(templates_dir,'searchform_dhcp.html'),
      u'DNS':os.path.join(templates_dir,'searchform_dns.html'),
      u'Kerberos':os.path.join(templates_dir,'searchform_mit_krb.html'),
      u'MS AD':os.path.join(templates_dir,'searchform_msad.html'),
    },

    # HTML template file for rename form
    rename_template= os.path.join(templates_dir,'rename.html'),

    # HTML template file for whole top section
    top_template=os.path.join(templates_dir,'top.html'),

    # HTML template file for password change form
    passwd_template=os.path.join(templates_dir,'passwd.html'),

    # HTML template file for Login form
    login_template=os.path.join(templates_dir,'login.html'),
    # Default mechanism for BindRequest (empty string for simple bind)
    login_default_mech='',

    # Attributes which should be present in attribute select list of advanced search form
    search_attrs=[],

    # There are some situations where this client just wants to get the
    # attributes of an entry and not the data itself for saving bandwidth.
    # However some LDAP hosts (e.g. Notes Domino 4.61) have problems with
    # such an attribute-only request, they won't return any matches for a search.
    # If you experience these problems (no matching entry) set this to 0.
    search_attrsonly=1,

    search_tablistattrs=['cn','mail','homephone','telephonenumber','mobile'],

    # HTML template strings used to display entries in the table
    # of search results
    search_tdtemplate= {
      'inetOrgPerson':r'%(entryDN)s<br>%(cn)s &lt;%(mail)s&gt;<br>Office: %(telephoneNumber)s, Home: %(homePhone)s, Mobile: %(mobile)s',
      'organization':r'%(entryDN)s<br>%(o)s Tel.: %(telephoneNumber)s',
      'organizationalUnit':r'%(entryDN)s<br>Org. Unit %(ou)s:<br>%(description)s',
      'rfc822MailGroup':r'Mailing list %(cn)s &lt;%(mail)s&gt;, see %(labeledurl)s',
      'account':r'%(entryDN)s<br>Account <strong>%(uid)s</strong>',
      'groupOfNames':r'%(entryDN)s<br>Group <strong>%(cn)s</strong>',
      'groupOfUniqueNames':r'%(entryDN)s<br>Group <strong>%(cn)s</strong>',
      'organizationalRole':r'%(entryDN)s<br>Role <strong>%(cn)s</strong>',
      'posixGroup':r'%(entryDN)s<br>POSIX group <strong>%(cn)s</strong> (%(gidNumber)s)',
      'namedObject':r'%(entryDN)s<br>Named object <strong>%(cn)s - %(uniqueIdentifier)s</strong><br>(%(displayName)s)',
      'sambaDomain':r'%(entryDN)s<br>Samba domain <strong>%(sambaDomainName)s</strong> (%(sambaSID)s)',
      'dnsDomain2':r"""%(entryDN)s<br>
        DNS RR <strong>%(associatedDomain)s</strong>:<br>
        A: %(aRecord)s<br>PTR: %(pTRRecord)s<br>CNAME: %(cNAMERecord)s
      """,
      'dhcpClass':r'%(entryDN)s<br>DHCP class <strong title="%(dhcpComments)s">%(cn)s</strong>',
      'dhcpGroup':r'%(entryDN)s<br>DHCP group <strong title="%(dhcpComments)s">%(cn)s</strong>',
      'dhcpHost':r'%(entryDN)s<br>DHCP host <strong title="%(dhcpComments)s">%(cn)s</strong><br>%(dhcpHWAddress)s',
      'dhcpServer':r'%(entryDN)s<br>DHCP server <strong title="%(dhcpComments)s">%(cn)s</strong>',
      'dhcpService':r'%(entryDN)s<br>DHCP service <strong title="%(dhcpComments)s">%(cn)s</strong>',
      'dhcpSharedNetwork':r'%(entryDN)s<br>DHCP shared network <strong title="%(dhcpComments)s">%(cn)s</strong>',
      'dhcpSubClass':r'%(entryDN)s<br>DHCP sub class <strong title="%(dhcpComments)s">%(cn)s</strong><br>%(dhcpClassData)s',
      'dhcpSubnet':r'%(entryDN)s<br>DHCP subnet <strong title="%(dhcpComments)s">%(cn)s/%(dhcpNetMask)s</strong>',
    },

    # Default for number of results shown per page
    search_resultsperpage=10,

    # Parameters for tree-viewer
    # Allow maximum this number of levels
    dit_max_levels=10,
    # Fetch at most this number of entries when searching below a node
    dit_search_sizelimit=50,
    # Timelimit [secs] for searching
    dit_search_timelimit=10,

    # HTML template file used for displaying entries of specific object class
    read_template={
      # 'object class':'pathname of HTML template file'
      'inetOrgPerson':os.path.join(templates_dir,'read_inetOrgPerson.html'),
      'account':os.path.join(templates_dir,'read_account.html'),
      'organizationalPerson':os.path.join(templates_dir,'read_inetOrgPerson.html'),
      'msPerson':os.path.join(templates_dir,'read_msPerson.html'),
      'organization':os.path.join(templates_dir,'read_organization.html'),
      'organizationalUnit':os.path.join(templates_dir,'read_organizationalUnit.html'),
      'msOrganization':os.path.join(templates_dir,'read_msOrganization.html'),
      'groupOfNames':os.path.join(templates_dir,'read_groupOfNames.html'),
      'posixAccount':os.path.join(templates_dir,'read_posixAccount.html'),
      'posixGroup':os.path.join(templates_dir,'read_posixGroup.html'),
      'eduPerson':os.path.join(templates_dir,'read_eduPerson.html'),
      'mailboxRelatedObject':os.path.join(templates_dir,'read_mailboxRelatedObject.html'),
      'namedObject':os.path.join(templates_dir,'read_namedObject.html'),
      'namedPolicy':os.path.join(templates_dir,'read_namedPolicy.html'),
      'pwdPolicy':os.path.join(templates_dir,'read_pwdPolicy.html'),
      'msPwdResetPolicy':os.path.join(templates_dir,'read_msPwdResetPolicy.html'),
      'sambaDomain':os.path.join(templates_dir,'read_sambaDomain.html'),
      'sambaSamAccount':os.path.join(templates_dir,'read_sambaSamAccount.html'),
      'sambaGroupMapping':os.path.join(templates_dir,'read_sambaGroupMapping.html'),
      'dhcpHost':os.path.join(templates_dir,'dhcp','read_dhcpHost.html'),
      'dhcpServer':os.path.join(templates_dir,'dhcp','read_dhcpServer.html'),
      'dhcpService':os.path.join(templates_dir,'dhcp','read_dhcpService.html'),
      'dhcpSubnet':os.path.join(templates_dir,'dhcp','read_dhcpSubnet.html'),
      'inetLocalMailRecipient':os.path.join(templates_dir,'read_inetLocalMailRecipient.html'),
      'oathHOTPUser':os.path.join(templates_dir,'oath','read_oathHOTPUser.html'),
      'oathTOTPUser':os.path.join(templates_dir,'oath','read_oathTOTPUser.html'),
      'oathHOTPToken':os.path.join(templates_dir,'oath','read_oathHOTPToken.html'),
      'oathTOTPToken':os.path.join(templates_dir,'oath','read_oathTOTPToken.html'),
      'oathParams':os.path.join(templates_dir,'oath','read_oathParams.html'),
      'oathHOTPParams':os.path.join(templates_dir,'oath','read_oathHOTPParams.html'),
      'oathTOTPParams':os.path.join(templates_dir,'oath','read_oathTOTPParams.html'),
    },

    # Maximum count of attribute values displayed when displaying a single entry
    # without attribute values being expanded
    read_tablemaxcount={
      'allowedAttributes':2,
      'allowedAttributesEffective':2,
      'allowedChildClasses':2,
      'allowedChildClassesEffective':2,
      'member':40,
      'memberOf':30,
      'memberUid':40,
      'pwdHistory':2,
      'roleOccupant':40,
      'tokenGroups':4,
      'tokenGroupsGlobalAndUniversal':4,
      'tokenGroupsNoGCAcceptable':4,
      'uniqueMember':40,
    },

    # HTML template file used for displaying input forms for entries
    # of specific object class
    input_template={
      # 'object class':'pathname of HTML template file'
      'inetOrgPerson':os.path.join(templates_dir,'inputform_inetOrgPerson.html'),
      'account':os.path.join(templates_dir,'inputform_account.html'),
      'msPerson':os.path.join(templates_dir,'inputform_msPerson.html'),
      'posixAccount':os.path.join(templates_dir,'inputform_posixAccount.html'),
      'posixGroup':os.path.join(templates_dir,'inputform_posixGroup.html'),
      'organization':os.path.join(templates_dir,'inputform_organization.html'),
      'organizationalUnit':os.path.join(templates_dir,'inputform_organizationalUnit.html'),
      'msOrganization':os.path.join(templates_dir,'inputform_msOrganization.html'),
      'groupOfNames':os.path.join(templates_dir,'inputform_groupOfNames.html'),
      'eduPerson':os.path.join(templates_dir,'inputform_eduPerson.html'),
      'mailboxRelatedObject':os.path.join(templates_dir,'inputform_mailboxRelatedObject.html'),
      'namedObject':os.path.join(templates_dir,'inputform_namedObject.html'),
      'namedPolicy':os.path.join(templates_dir,'inputform_namedPolicy.html'),
      'pwdPolicy':os.path.join(templates_dir,'inputform_pwdPolicy.html'),
      'msPwdResetPolicy':os.path.join(templates_dir,'inputform_msPwdResetPolicy.html'),
      'sambaDomain':os.path.join(templates_dir,'inputform_sambaDomain.html'),
      'sambaSamAccount':os.path.join(templates_dir,'inputform_sambaSamAccount.html'),
      'sambaGroupMapping':os.path.join(templates_dir,'inputform_sambaGroupMapping.html'),
      'dhcpHost':os.path.join(templates_dir,'dhcp','inputform_dhcpHost.html'),
      'dhcpServer':os.path.join(templates_dir,'dhcp','inputform_dhcpServer.html'),
      'dhcpService':os.path.join(templates_dir,'dhcp','inputform_dhcpService.html'),
      'dhcpSubnet':os.path.join(templates_dir,'dhcp','inputform_dhcpSubnet.html'),
      'dNSDomain2':os.path.join(templates_dir,'inputform_dNSDomain2.html'),
      'inetLocalMailRecipient':os.path.join(templates_dir,'inputform_inetLocalMailRecipient.html'),
      'oathHOTPUser':os.path.join(templates_dir,'oath','inputform_oathHOTPUser.html'),
      'oathTOTPUser':os.path.join(templates_dir,'oath','inputform_oathTOTPUser.html'),
      'oathHOTPToken':os.path.join(templates_dir,'oath','inputform_oathHOTPToken.html'),
      'oathTOTPToken':os.path.join(templates_dir,'oath','inputform_oathTOTPToken.html'),
      'oathParams':os.path.join(templates_dir,'oath','inputform_oathParams.html'),
      'oathHOTPParams':os.path.join(templates_dir,'oath','inputform_oathHOTPParams.html'),
      'oathTOTPParams':os.path.join(templates_dir,'oath','inputform_oathTOTPParams.html'),
    },

    # HTML template file used for displaying operational attributes
    # in a footer when displaying a single entry
    read_operationalattrstemplate=os.path.join(templates_dir,'read_operationalattrs.html'),

    # Number of columns for print output
    print_cols=4,

    # Parameters for password generation
    # Unicode string containing all valid characters used when generating
    # password values
    passwd_genchars=ur'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
    # Length of generated password
    passwd_genlength=24,

    # Dictionary { description : LDIF file name } for displaying
    # link for quickly choosing LDIF templates for new entries
    addform_entry_templates={
      u'Person / Contact':os.path.join(templates_dir,'add_person.ldif'),
      u'Organization (Company etc.)':os.path.join(templates_dir,'add_organization.ldif'),
      u'Organizational Unit':os.path.join(templates_dir,'add_orgunit.ldif'),
      u'Group':os.path.join(templates_dir,'add_group.ldif'),
      u'Locality':os.path.join(templates_dir,'add_locality.ldif'),
      u'POSIX user':os.path.join(templates_dir,'add_user.ldif'),
      u'Mail user':os.path.join(templates_dir,'add_mailaccount.ldif'),
      u'DNS sub-domain':os.path.join(templates_dir,'add_dnsdomain2.ldif'),
      u'DNS zone (SOA)':os.path.join(templates_dir,'add_dnsdomain2_soa.ldif'),
      u'Application process':os.path.join(templates_dir,'add_applicationprocess.ldif'),
    },

    # HTML template strings used to display the superior entry
    # in the input form when adding/modifying entries
    inputform_supentrytemplate={
      'organization':r'Organization <strong>%(o)s</strong>',
      'organizationalUnit':r'Organizational Unit <strong>%(ou)s</strong>',
    },

    # Named set of LDAP URLs for searching new superior DN when renaming an entry
    rename_supsearchurl={
      u'Search current naming context for organizationalUnit':'ldap:///_??sub?(objectClass=organizationalUnit)',
      u'Search current naming context for organization':'ldap:///_??sub?(objectClass=organization)',
      u'Search current naming context for locality':'ldap:///_??sub?(objectClass=locality)',
      u'Search current naming context for domain':'ldap:///_??sub?(objectClass=domain)',
      u'Search below superior entry for organizationalUnit':'ldap:///..??sub?(objectClass=organizationalUnit)',
      u'Search below superior entry for organization':'ldap:///..??sub?(objectClass=organization)',
      u'Search below superior entry for locality':'ldap:///..??sub?(objectClass=locality)',
      u'Search below superior entry for domain':'ldap:///..??sub?(objectClass=domain)',
    },

    # LDIF file used as locally stored pseudo LDAPv3 schema
    schema_uri='file:'+os.path.join(etc_dir,'localschema.ldif'),

    # Whether to apply strict subschema consistency check (e.g. uniqueness)
    schema_strictcheck=True,

    # The definitions for group entry administration
    groupadm_filterstr_template=r'(|%s)',
    groupadm_optgroup_bounds=(1,None),
    groupadm_defs={
      'groupOfNames':       ('member',None),
      'groupOfUniqueNames': ('uniqueMember',None),
      'organizationalRole': ('roleOccupant',None),
      'rfc822MailGroup':    ('mail','mail'),
      'nisMailAlias':       ('rfc822MailMember','mail'),
      'mailGroup':          ('mgrprfc822mailmember','mail'),
      # Found on IBM SecureWay Directory
      'accessGroup':        ('member',None),
      # RFC2370
      'posixGroup':         ('memberUid','uid'),
      'nisNetgroup':        ('memberNisNetgroup','uid'),
      # Samba 3.0
#      'sambaGroupMapping':  ('sambaSIDList','sambaSID'),
      # Active Directory
      'group':              ('member',None),
      # draft-findlay-ldap-groupofentries
      'groupOfEntries':     ('member',None),
      # Apple MAC OS X
      'apple-group':        ('apple-group-memberguid','apple-generateduid'),
    },

  ),

  'ldap://localhost': Web2LDAPConfig(
    description=u'My poorly configured LDAP host',
  ),

  'ldap://localhost:7389': Web2LDAPConfig(
    description=u'Sun/Oracle DSEE',
    # broken schema shipped with Sun/Oracle/389 DS
    schema_strictcheck=False,
  ),

  'ldap://ipa.demo1.freeipa.org': Web2LDAPConfig(
    description=u'freeIPA demo host',
    # work around 389-DS bug here
    schema_strictcheck=False,
  ),

  # This meant as an more complex example section
  # Adjust the settings to reflect your local LDAP installation
  'ldapi://%2Ftmp%2Fopenldap-socket/dc=stroeder,dc=de': Web2LDAPConfig(
    description=u'My Address Book',
    session_track_control=1,
    # LDIF file used to extended the server's schema
#    schema_supplement=os.path.join(etc_dir,'stroeder-dit-structure.ldif'),
    searchform_search_root_url=u'ldap:///dc=stroeder,dc=de??sub?(&(|(ou=Private)(ou:dn:=Bizness)(ou:dn:=Kultur))(|(objectClass=msOrganization)(objectClass=organizationalUnit))(hasSubordinates=TRUE)(|(organizationalStatus=0)(!(organizationalStatus=*))))',
    search_attrs=[
      'authTimestamp','createTimestamp','creatorsName','modifiersName','modifyTimestamp',
      'cn','mail','sn','givenName','personalTitle','businessTitle','gender',
      'o','ou','departmentNumber','employeeNumber',
      'telephoneNumber','homePhone','mobile',
      'c','st','l','streetAddress','roomNumber','postalCode',
      'uid','uidNumber','description',
      'objectClass','organizationalStatus',
      'entryDN','entryUUID',
      # DNS
      'dc','associatedDomain','mXRecord','aRecord','aAAARecord','pTRRecord','nSRecord','sOARecord',
      # groups
      'member','memberOf',
      # DHCP
      'dhcpHWAddress','dhcpOption','dhcpStatements',
    ],
    addform_entry_templates={
      u'stroeder.com Person':os.path.join(templates_dir,'add_msperson.ldif'),
      u'stroeder.com Organization':os.path.join(templates_dir,'add_msorganization.ldif'),
      u'User':os.path.join(templates_dir,'add_user.ldif'),
      u'Organizational unit (OU)':os.path.join(templates_dir,'add_orgunit.ldif'),
      u'Group':os.path.join(templates_dir,'add_group.ldif'),
      u'Posix user account':os.path.join(templates_dir,'add_user.ldif'),
      u'DNS sub-domain':os.path.join(templates_dir,'add_dnsdomain2.ldif'),
      u'DNS zone (SOA)':os.path.join(templates_dir,'add_dnsdomain2_soa.ldif'),
      u'DHCP host':os.path.join(templates_dir,'dhcp','add_dhcpHost.ldif'),
      u'DHCP server':os.path.join(templates_dir,'dhcp','add_dhcpServer.ldif'),
      u'DHCP service':os.path.join(templates_dir,'dhcp','add_dhcpService.ldif'),
      u'DHCP subnet':os.path.join(templates_dir,'dhcp','add_dhcpSubnet.ldif'),
      u'X.509 CA':os.path.join(templates_dir,'add_pkica.ldif'),
    },
#    login_default_mech='EXTERNAL',
#    passwd_hashtypes=['ssha',''],
#    schema_uri='ldapi://%2Ftmp%2Fopenldap-socket/cn=Subschema',
#    schema_uri='file:'+os.path.join(etc_dir,'localschema.ldif'),
  ),

  # Example for OpenLDAP's accesslog database
  'ldap:///cn=accesslog': openldap_accesslog_config,

  # Example for changelog database
  'ldap:///cn=changelog': changelog_config,

  # Example for cn=Monitor covering various server implementations
  'ldap:///cn=Monitor': openldap_monitor_config,

  # For dynamic configuration via cn=config
  'ldap:///cn=config': cn_config,

  # Æ-DIR's main DB
  'ldap:///ou=ae-dir': ae_dir_config,

  # Æ-DIR's accesslog
  'ldap:///cn=accesslog-ae-dir': openldap_accesslog_config,

  # Æ-DIR's online demo
  'ldaps://demo.ae-dir.com': Web2LDAPConfig(
    description=u'AE-DIR demo',
    tls_options={
      ldap0.OPT_X_TLS_CACERTFILE:os.path.join(etc_dir,'ssl','crt','DST_Root_CA_X3.pem'),
    },
  )

}

# You can apply sections defined above to other configuration keys
ldap_def['ldap://demo.ae-dir.com'] = ldap_def['ldaps://demo.ae-dir.com']

ldap_def['ldap:///dc=stroeder,dc=local'] = ldap_def['ldapi://%2Ftmp%2Fopenldap-socket/dc=stroeder,dc=de']
ldap_def['ldap:///dc=stroeder,dc=de'] = ldap_def['ldapi://%2Ftmp%2Fopenldap-socket/dc=stroeder,dc=de']
