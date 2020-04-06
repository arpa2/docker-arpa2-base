/* Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "ap_config.h"
#include "ap_mmn.h"
#include "httpd.h"
#include "http_config.h"
#include "http_connection.h"
#include "http_core.h"
#include "http_log.h"
#include "http_vhost.h"
#include "http_request.h"
#include "apr_strings.h"

#include <sasl/sasl.h>
#include <sasl/saslplug.h>
#include <sasl/saslutil.h>

#include <pcre.h>

#define SAMPLE_SEC_BUF_SIZE (2048)


#define RE_SASL_MECH "[A-Z0-9-_]{1,20}"
#define RE_MECHSTRING "\"(" RE_SASL_MECH "(?:[ ]" RE_SASL_MECH ")*)\""
#define RE_DNSSTRING  "\"([a-zA-Z0-9-_]+(?:\\.[a-zA-Z0-9-_]+)+)\""
#define RE_BWS  "[ \\t]*"
#define RE_OWS  RE_BWS
#define RE_TOKEN68  "([a-zA-Z0-9-._~+/]+=*)"
#define RE_AUTH_PARAM \
    "(?:" \
        "([CcSs][2][CcSs])" RE_BWS "=" RE_BWS RE_TOKEN68 \
        "|" \
        "([Mm][Ee][Cc][Hh])" RE_BWS "=" RE_BWS RE_MECHSTRING \
        "|" \
        "([Rr][Ee][Aa][Ll][Mm])" RE_BWS "=" RE_BWS RE_DNSSTRING \
    ")"
#define RE_AUTH_SCHEME  "[Ss][Aa][Ss][Ll]"
#define RE_CREDENTIALS  RE_AUTH_SCHEME "(?:[ ]+(" RE_AUTH_PARAM "(?:" \
    RE_OWS "," RE_OWS RE_AUTH_PARAM ")+)?)"

module AP_MODULE_DECLARE_DATA sasl_module;

typedef struct {
    char *realm;
} sasl_dir_config;

typedef enum {
    cmd_saslrealm
} cmd_parts;

char buf[SAMPLE_SEC_BUF_SIZE];

static void trace_nocontext(apr_pool_t *p, const char *file, int line,
                            const char *note)
{
    /*
     * Since we have no request or connection to trace, or any idea
     * from where this routine was called, there's really not much we
     * can do.  If we are not logging everything by way of the
     * EXAMPLE_LOG_EACH constant, do nothing in this routine.
     */

    ap_log_perror(file, line, APLOG_MODULE_INDEX, APLOG_NOTICE, 0, p,
                  APLOGNO(03297) "%s", note);
}

/*
 * Locate our directory configuration record for the current request.
 */
static sasl_dir_config *our_dconfig(const request_rec *r)
{
    return (sasl_dir_config *) ap_get_module_config(r->per_dir_config, &sasl_module);
}

static int
sasl_my_log(void *context __attribute__((unused)),
            int priority,
            const char *message) 
{
    const char *label;

    if (! message)
        return SASL_BADPARAM;

    switch (priority) {
    case SASL_LOG_ERR:
        label = "Error";
        break;
    case SASL_LOG_NOTE:
        label = "Info";
        break;
    default:
        label = "Other";
        break;
    }

    apr_pool_t *p = (apr_pool_t*) context;
    char *note = apr_psprintf(
        p, "SASL %s: %s", label, message);
    trace_nocontext(p, __FILE__, __LINE__, note);

    return SASL_OK;
}

static sasl_callback_t callbacks[] = {
  {
    SASL_CB_LOG, (sasl_callback_ft)&sasl_my_log, NULL
  }, {
    SASL_CB_LIST_END, NULL, NULL
  }
};

static void *create_sasl_dir_config(apr_pool_t *p, char *dirspec)
{
    sasl_dir_config *pConfig = apr_pcalloc(p, sizeof *pConfig);

    char *note = apr_psprintf(p, "create_sasl_dir_config(p == %pp, dirspec == %s)",
                        (void*) p, dirspec);
    callbacks[0].context = p;
    trace_nocontext(p, __FILE__, __LINE__, note);
    return pConfig;
}

sasl_conn_t *conn = NULL;
int state = 0; // temporary
pcre *re_credentials;
pcre *re_auth_parm;

static int list_mech(const char **result_string, unsigned *string_length, int *number_of_mechanisms)
{
    int result;

    state = 0;
    result = sasl_listmech(
        conn,  /* The context for this connection */
        NULL,  /* not supported */
        NULL,  /* What to prepend the string with */
        " ",   /* What to separate mechanisms with */
        NULL,  /* What to append to the string */
        result_string, /* The produced string. */
        string_length, /* length of the string */
        number_of_mechanisms /* Number of mechanisms in
                                the string */
    );
    return result;
}

#ifdef HTTP_HACK
static sasl_http_request_t httpreq =
{
    "AUTHENTICATE",	/* Method */
    NULL,		    /* URI */
    NULL,	        /* Empty body */
    0,			    /* Zero-length body */
    0               /* Persistent cxn */
};
#endif

static const char *sasl_param(cmd_parms *cmd, void *dconf, const char *val)
{
    sasl_dir_config *pConfig = (sasl_dir_config *) dconf; 

    switch ((long) cmd->info) {
        case cmd_saslrealm: {
            pConfig->realm = apr_pstrdup(cmd->pool, val);
            char *note = apr_psprintf(cmd->pool, "sasl_param: realm = %s", pConfig->realm);
            trace_nocontext(cmd->pool, __FILE__, __LINE__, note);
            int result = sasl_server_init(callbacks, "http-sasl");
            if (result == SASL_OK) {
                if (conn) {
                    sasl_dispose(&conn);
                }
                result = sasl_server_new(
                    "HTTP",
                    NULL,           /* my fully qualified domain name;
                                       NULL says use gethostname() */
                    val,            /* The user realm used for password
                                       lookups; NULL means default to serverFQDN
                                       Note: This does not affect Kerberos */
                    NULL, NULL,     /* IP Address information strings */
                    NULL,           /* Callbacks supported only for this connection */
#ifdef HTTP_HACK
                    SASL_NEED_HTTP, /* security flags (security layers are enabled
                                       using security properties, separately) */
#else
                    0,              /* security flags (security layers are enabled
                                       using security properties, separately) */
#endif
                    &conn
                );
#ifdef HTTP_HACK
                /* Set HTTP request as specified above (REQUIRED) */
                sasl_setprop(conn, SASL_HTTP_REQUEST, &httpreq);
#endif
            }
        }
        break;
    }
    return NULL;
}

static const command_rec sasl_cmds[] = {
    AP_INIT_TAKE1("AuthName", sasl_param, (void*)cmd_saslrealm, OR_AUTHCFG,
                  "SASL realm"),
    {NULL}
};

#define OVECCOUNT 30    /* should be a multiple of 3 */
static int ovector[OVECCOUNT];

static apr_hash_t* parse_authorization_header(apr_pool_t *p, const char *auth_line)
{
    apr_hash_t* hash = NULL;
    int rc = pcre_exec(
        re_credentials,    /* the compiled pattern */
        NULL,              /* no extra data - we didn't study the pattern */
        auth_line,         /* the subject string */
        strlen(auth_line), /* the length of the subject */
        0,                 /* start at offset 0 in the subject */
        0,                 /* default options */
        ovector,           /* output vector for substring information */
        OVECCOUNT          /* number of elements in the output vector */
    );
    if (rc >= 0) {
        int start_offset = 0;
        hash = apr_hash_make(p);

        for (;;) {
            rc = pcre_exec(
                re_auth_parm,      /* the compiled pattern */
                NULL,              /* no extra data - we didn't study the pattern */
                auth_line,         /* the subject string */
                strlen(auth_line), /* the length of the subject */
                start_offset,      /* start at offset 0 in the subject */
                0,                 /* default options */
                ovector,           /* output vector for substring information */
                OVECCOUNT          /* number of elements in the output vector */
            );
            if (rc > 0) {
                char *key = NULL;
                char *value = NULL;
                int i;

                for (i = 1; i < rc; i++) {
                    int substring_length = ovector[2 * i + 1] - ovector[2 * i];
                    if (substring_length > 0)
                    {
                        const char *substring_start = auth_line + ovector[2 * i];
                        if (key == NULL) {
                            key = apr_pmemdup(p, substring_start, substring_length + 1);
                            key[substring_length] = '\0';
                        } else if (value == NULL) {
                            value = apr_pmemdup(p, substring_start, substring_length + 1);
                            value[substring_length] = '\0';
                            apr_hash_set(hash, key, APR_HASH_KEY_STRING, value);
                            char *note = apr_psprintf(p, "adding ('%s', '%s')", key, value);
                            trace_nocontext(p, __FILE__, __LINE__, note);
                        }
                    }
                }
                start_offset = ovector[1];
            } else {
                trace_nocontext(p, __FILE__, __LINE__, "no (more) auth param matches");
                break;
            }
        }
    } else {
        trace_nocontext(p, __FILE__, __LINE__, "no credentials match");
    }
    return hash;
}


static void send_mechs(request_rec *r)
{
    const char *result_string;
    unsigned string_length;
    int number_of_mechanisms;

    if (list_mech(&result_string, &string_length, &number_of_mechanisms) == SASL_OK) {
        sasl_dir_config *dconf = our_dconfig(r);
        apr_table_setn(
            r->err_headers_out,
            (PROXYREQ_PROXY == r->proxyreq) ? "Proxy-Authenticate" : "WWW-Authenticate",
            apr_pstrcat(
                r->pool,
                "SASL mech=\"",
                 result_string,
                 "\",realm=\"",
                 /*dconf->realm*/ "test-realm.nl",
                 "\"",
                 NULL
            )
        );
    }
}

/*
 * This routine is called to check for any module-specific restrictions placed
 * upon the requested resource.  (See the mod_access_compat module for an
 * example.)
 *
 * This is a RUN_ALL hook. The first handler to return a status other than OK
 * or DECLINED (for instance, HTTP_FORBIDDEN) aborts the callback chain.
 */
static int sasl_check_access(request_rec *r)
{
    const char *auth_line;
    int rc = PROXYREQ_PROXY == r->proxyreq
            ? HTTP_PROXY_AUTHENTICATION_REQUIRED
            : HTTP_UNAUTHORIZED;

    trace_nocontext(r->pool, __FILE__, __LINE__, "sasl_check_access");
    /* Get the appropriate header */
    auth_line = apr_table_get(
        r->headers_in,
        (PROXYREQ_PROXY == r->proxyreq) ? "Proxy-Authorization" : "Authorization"
    );
    if (auth_line) {
        char *note = apr_psprintf(r->pool, "auth_line = %s", auth_line);
        trace_nocontext(r->pool, __FILE__, __LINE__, note);
        switch (state) {
            case 0: { // mechanisms sent
                apr_hash_t *hash = parse_authorization_header(r->pool, auth_line);
                char *mech = apr_hash_get(hash, "mech", APR_HASH_KEY_STRING);
                note = apr_psprintf(r->pool, "mech = %s", mech);
                trace_nocontext(r->pool, __FILE__, __LINE__, note);
                char *c2s_base64 = apr_hash_get(hash, "c2s", APR_HASH_KEY_STRING);
                note = apr_psprintf(r->pool, "c2s_base64 = %s", c2s_base64);
                trace_nocontext(r->pool, __FILE__, __LINE__, note);
                const char *clientin = NULL;
                unsigned clientinlen = 0;
                const char *serverout;
                unsigned serveroutlen;
                int result;
                if (c2s_base64) {
                    result = sasl_decode64(
                        c2s_base64,
                        (unsigned) strlen(c2s_base64),
                        buf,
                        SAMPLE_SEC_BUF_SIZE,
                        &clientinlen);
                    if (result == SASL_OK) {
                        clientin = buf;
                        note = apr_psprintf(r->pool, "c2s = %s", clientin);
                        trace_nocontext(r->pool, __FILE__, __LINE__, note);
                    }
#ifdef HTTP_HACK
                    result = sasl_server_start(conn, mech, clientin, clientinlen, &serverout, &serveroutlen);
#else
                    result = sasl_server_step(conn, clientin, clientinlen, &serverout, &serveroutlen);
#endif
                } else {
                    result = sasl_server_start(conn, mech, NULL, 0, &serverout, &serveroutlen);
                }
                if (result != SASL_OK && result != SASL_CONTINUE) {
                    note = apr_psprintf(r->pool, "Error starting SASL negotiation: %s", sasl_errstring(result, NULL, NULL));
                } else {
                    note = apr_psprintf(r->pool, "result = %d, serverout = %s, serveroutlen = %d", result, serverout, serveroutlen);
                    int len;
                    if (result == SASL_OK) {
                        rc = OK;
                    } else {
                        result = sasl_encode64(serverout, serveroutlen, buf, SAMPLE_SEC_BUF_SIZE, &len);
                        if (result == SASL_OK)
                        {
                            apr_table_setn(
                                r->err_headers_out,
                                (PROXYREQ_PROXY == r->proxyreq) ? "Proxy-Authenticate" : "WWW-Authenticate",
                                apr_pstrcat(
                                    r->pool,
                                    "SASL mech=\"",
                                    mech,
                                    "\",realm=\"",
                                    /*dconf->realm*/ "test-realm.nl",
                                    "\",s2c=",
                                    buf,
                                     ",s2s=1",
                                     NULL
                                )
                            );
                        }
                    }
                }
                trace_nocontext(r->pool, __FILE__, __LINE__, note);
                break;
            }
        }
    } else {
        trace_nocontext(r->pool, __FILE__, __LINE__, "No authorization header");
        send_mechs(r);
    }
    return rc;
}

static void check_re(apr_pool_t *p, const pcre *re, const char *error, int erroffset)
{
    /* Compilation failed: print the error message and exit */
    if (re == NULL)
    {
        char *note = apr_psprintf(p, "PCRE compilation failed at offset %d: %s\n", erroffset, error);
        trace_nocontext(p, __FILE__, __LINE__, note);
    }
}

static void register_hooks(apr_pool_t *p)
{
    const char *error;
    int erroffset;

    re_credentials = pcre_compile(
        RE_CREDENTIALS, /* the pattern */
        0,              /* default options */
        &error,         /* for error message */
        &erroffset,     /* for error offset */
        NULL            /* use default character tables */
    );
    check_re(p, re_credentials, error, erroffset);
    re_auth_parm = pcre_compile(
        RE_AUTH_PARAM,  /* the pattern */
        0,              /* default options */
        &error,         /* for error message */
        &erroffset,     /* for error offset */
        NULL            /* use default character tables */
    );
    check_re(p, re_auth_parm, error, erroffset);

    ap_hook_check_access(
        sasl_check_access,
        NULL,
        NULL,
        APR_HOOK_MIDDLE,
        AP_AUTH_INTERNAL_PER_CONF
    );
}

AP_DECLARE_MODULE(sasl) = {
    STANDARD20_MODULE_STUFF,
    create_sasl_dir_config,        /* create per-directory config structure */
    NULL,                          /* merge per-directory config structures */
    NULL,                          /* create per-server config structure */
    NULL,                          /* merge per-server config structures */
    sasl_cmds,                     /* command apr_table_t */
    register_hooks                 /* register hooks */
};
