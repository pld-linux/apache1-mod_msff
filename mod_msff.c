/*
 * mod_msff.c: Microsoft Free Fridays: reject MSIE on Friday.
 *
 * Michael Anthony <m@beanpod.net>
 * You may use this software free for any purpose.
 * It has no warranty.
 *
 * You might find success by trying to build it like this:
 *
 *     gcc -c -I<apache include dir> -fpic -DSHARED_MODULE mod_msff.c
 *     gcc -shared -o mod_msff.so mod_msff.o
 *
 * But you also might not.  After you do that, you'll want the
 * resulting .so file in your Apache installation's libexec directory.
 *
 * Enable the module by putting this line right around where the
 * LoadModule line for mod_auth is:
 *
 *     LoadModule msff_module libexec/mod_msff.so
 *
 * and put this line right around where the AddModule line for
 * mod_auth is:
 *
 *     AddModule mod_msff.c
 *
 */

#include "httpd.h"
#include "http_core.h"
#include "http_config.h"
#include "http_log.h"
#include "http_request.h"
#include <string.h>
#include <ctype.h>

static void dump_message (request_rec *r)
{
    r->content_type = "text/html";
    r->status = FORBIDDEN;
    ap_send_http_header (r);

    if (! r->header_only)
    {
        ap_rprintf (
            r,
            "<html xml:lang=\"en\" lang=\"en\">\n"
            "<head>\n"
            "<title>Go home, Billy!</title>\n"
            "</head>\n"
            "<body>\n"
            "<p><h1>Happy "
            "<a href=\"http://davenet.userland.com/2001/06/13\">"
            "Microsoft-Free Friday</a>!</h1></p>\n"
            "<p>In support of freedom of choice in browser software, this"
            " web site is Microsoft-Free on Fridays.  Please use any"
            " browser except MSIE to access this web site today.</p>\n"
            "</body>\n"
            "</html>\n");
    }
}

static int msff (request_rec *r)
{
    int ret = 0;
    time_t now;
    struct tm *tmp;
    char *agent = 0;
    const char *foo;
    char *p;

    foo = ap_table_get (r->headers_in, "User-Agent");
    if (foo)
    {
        agent = ap_pstrdup (r->pool, foo);
        for (p = agent; *p; ++p)
        {
            if (isupper (*p))
            {
                *p = tolower (*p);
            }
        }
    }

    if (agent
        && strstr (agent, "msie")
        && ! strstr (agent, "opera")
        && ! strstr (agent, "oregano"))
    {
        time (&now);
        tmp = localtime (&now);
        if (tmp->tm_wday == 5)
        {
            ret = 1;
        }
    }

    return ret;
}

static int handle_msff (request_rec *r)
{
    if (msff (r))
    {
        dump_message (r);
        return OK;
    }
    else
    {
        return DECLINED;
    }
}

module MODULE_VAR_EXPORT msff_module;

static const command_rec msff_cmds[] =
{
    { NULL }
};

static const handler_rec msff_handlers[] =
{
    { "*/*", handle_msff },
    { NULL }
};

module MODULE_VAR_EXPORT msff_module =
{
    STANDARD_MODULE_STUFF,
    NULL,           /* initializer */
    NULL,           /* dir config creater */
    NULL,           /* dir merger --- default is to override */
    NULL,           /* server config */
    NULL,           /* merge server config */
    msff_cmds,      /* command table */
    msff_handlers,  /* handlers */
    NULL,           /* filename translation */
    NULL,           /* check_user_id */
    NULL,           /* check auth */
    NULL,           /* check access */
    NULL,           /* type_checker */
    NULL,           /* fixups */
    NULL,           /* logger */
    NULL,           /* header parser */
    NULL,           /* child_init */
    NULL,           /* child_exit */
    NULL            /* post read-request */
};
