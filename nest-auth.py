#!/usr/bin/python

import nest
import json

print ("Nest Authenticator")
client_id = raw_input("Client ID: ")
client_secret = raw_input("Client Secret: ")
access_token_cache_file = '/opt/nest.json'

napi = nest.Nest(client_id=client_id, client_secret=client_secret, access_token_cache_file=access_token_cache_file)

if napi.authorization_required:
    print('Go to ' + napi.authorize_url + ' to authorize, then enter PIN below')
    pin = raw_input("PIN: ")
    napi.request_token(pin)

    with open('/opt/nest-config.json', 'w') as fp:
        json.dump({'client_id':client_id, 'client_secret':client_secret, 'access_token_cache_file':access_token_cache_file}, fp)
else:
    print ("Already Authorized")

