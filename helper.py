#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     14/04/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import requests
import requests.exceptions
import json
import os
import sys



def claim_key(key_filepath, host_name):
    # Claim the new key
    allocate_url = host_name + '/api/v1.0/allocate_key'
    response = requests.get(allocate_url)
    data = response.json()
    if not data['success']:
        raise Exception('Failed to claim API key')
    api_key = data['api_key']
    # Save it to a file
    with open(key_filepath, 'w') as f:
        f.write(json.dumps({'api_key':api_key}))
    return api_key


def release_key(key_filepath, host_name):
    # Load the old key
    if not os.path.exists(key_filepath):
        return
    with open(key_filepath, 'r') as f:
        file_raw = f.read()
    file_decoded = json.loads(file_raw)
    api_key = file_decoded['api_key']
    # Release it
    deallocate_url = host_name + '/api/v1.0/deallocate_key'
    response = requests.post(deallocate_url, json={'api_key':api_key})
    data = response.json()
    if not data['success']:
        raise Exception('Failed to release API key')
    # Erase key file
    with open(key_filepath, 'w') as f:
        f.write('{}')
    return



def main():
    #return claim_key(key_filepath='api_key.json', host_name='http://127.0.0.1:5000')#TODO REMOVEME
    #return release_key(key_filepath='api_key.json', host_name='http://127.0.0.1:5000')#TODO REMOVEME
    command = sys.argv[1]
    disco_tracker = os.environ['disco_tracker']
    item_dir = os.environ['item_dir']

    key_filepath = os.path.join(item_dir, 'api_key.json')

    if command == 'claim':
        claim_key(key_filepath='api_key.json', host_name=disco_tracker)

    elif command == 'release':
        release_key(key_filepath='api_key.json', host_name=disco_tracker)

    else:
        raise Exception('Unknown command.')

    return


if __name__ == '__main__':
    main()
