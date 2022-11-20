#!/usr/bin/python

import nest
import json

print ("Nest Authenticator")
project_id = input("Project ID: ")
client_id = input("Client ID: ")
client_secret = input("Client Secret: ")
access_token_cache_file = '/opt/nest.json'

def reauthorize_callback(url):
    print("Go here and follow the instructions")
    print(url)
    result_url = input("Paste the final url you landed on from Google's auth flow (e.g.google.com?state=...): ")
    return result_url

with nest.Nest(client_id=client_id, client_secret=client_secret, project_id=project_id, access_token_cache_file=access_token_cache_file, reautherize_callback=reauthorize_callback) as napi:
    # Will trigger initial auth and fetch of data
    devices = napi.get_devices()
    print(devices)
    with open('/opt/nest-config.json', 'w') as fp:
        json.dump({'project_id': project_id, 'client_id':client_id, 'client_secret':client_secret, 'access_token_cache_file':access_token_cache_file}, fp)
