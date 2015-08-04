#!/usr/bin/python

from urlparse import urlparse
import httplib, json
import os

# Constant definitions.
USER=os.environ.get('OS_USERNAME')
PASSWORD=os.environ.get('OS_PASSWORD')
PUBLIC_URL=os.environ.get('OS_AUTH_URL')

# 
TOKEN_ID="token-id"
USER_ID="user-id"
HTTP_OK=200

def do_http_req(method, url, headers, payload):
    """ Do an HTTP Request """
    parsed_url=urlparse(url)

    #print url
    #print headers
    #print payload

    con=httplib.HTTPConnection(parsed_url.netloc)
    con.request(method, parsed_url.path, payload, headers)
    return con.getresponse()


def get(url, headers):
    """ GET wrapper for "do_http_request """
    return do_http_req("GET", url, headers, None)


def post(url, headers, payload):
    """ POST wrapper for "do_http_request """
    return do_http_req("POST", url, headers, payload)


def get_token_id():
    """ Given an user and a password we get a token-id and an user id.

    Keuword arguments:
    user -- The user (email) valid for Keyrock
    password -- The password valid for the user

    Returns a dictionary (in order to be comprenhesible) with 2 values d["user-id"] and d["token-id"].
    Howerver, if the dictionary values are None an error has occured.
    """
    # Variable declarions.
    res={TOKEN_ID: None, USER_ID: None}
    dict_data={"auth": {"passwordCredentials": {"username": USER, "password": PASSWORD}}}
    payload=json.dumps(dict_data)
    headers={"Content-type": "application/json"}
    url="%s/tokens" % (PUBLIC_URL)

    # Do the POST
    response=post(url, headers, payload)

    # Prepare the response if OK
    if response.status == HTTP_OK:
        response_data=response
        info=json.loads(response.read())
        res[TOKEN_ID]=info['access']['token']['id']
        res[USER_ID]=info['access']['user']['id']

    return res


def get_tenants(tokens):
    """Given a TOKEN_ID returned from "get_token_id", we look for the tenants

    returns an array of tenants which the user belongs to or None if error
    """
    # Variable declarations
    tenants=None
    headers={"x-auth-token": tokens[TOKEN_ID], "Content-type": "application/json"}
    url="%s/tenants" % (PUBLIC_URL)
     
    # Do the POST
    response=get(url, headers)
    if response.status == HTTP_OK:
        response_data=json.loads(response.read())
        tenants=map(lambda x : x['id'], response_data['tenants'])
     
    return tenants


def select_tenant(tenants):
    """Ask the user their tenant if there are serveral tenants
    
    Returns tenant_id or None if error
    """
    #print "\n\n"
    tenant=None
    i=0
    if len(tenants)>1:
        print "Several tenants found..."
        for t in tenants:
            print "%d : %s" % (i, t)
            i+=1

    try:
       n_tenant=0
       if len(tenants)>1:
           n_tenant=raw_input("Choose your tenant [%d-%d]:" % (0,i-1))
       tenant=tenants[int(n_tenant)]
    except:
        pass

    return tenant


def get_token(tokens, tenant):
    """Get the "valid token" to query Openstack

    Returns a valid token for a token-id and a tenant. None if error
    """

    token=None
    headers={"Content-type": "application/json"}
    dict_data={"auth": {"token": {"id": tokens[TOKEN_ID]}, "tenantId": tenant}}
    payload=json.dumps(dict_data)
    
    response=post("%s/tokens" % (PUBLIC_URL), headers, payload)

    if response.status == HTTP_OK: 
        keystone_info=json.loads(response.read())  # Plenty of information
        token=keystone_info['access']['token']['id']
    return token

def usage():
    print "This scripts returns one token for each tenant the user belongs to"
    print 
    print "You should set the variables OS_USERNAME, OS_PASSWORD, OS_AUTH_URL before running this script..."
    print "export OS_USERNAME=jhon.doe@example.com"
    print "export OS_PASSWORD=whatever"
    print "export OS_AUTH_URL=http://cloud.lab.fiware.org:4730/v2.0"
    print "\n\nsimple_token.py"
    print "<tenant_1> <token_1>"
    print "...."
    print "<tenant_n> <token_n>"

if __name__ == "__main__":
    tokens=get_token_id()
    if tokens[TOKEN_ID] == None: # ERROR - Failure
        usage()
        exit(1)

    tenants=get_tenants(tokens)

    # tenant=select_tenant(tenants)
    # if tenant == None:
    #    exit(1)
    for tenant in tenants:
        print tenant, get_token(tokens, tenant)
