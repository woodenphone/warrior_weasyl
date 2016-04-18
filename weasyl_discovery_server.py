#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     12/04/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logging
import json
import base64
import time
import pickle


from logins import *# logins.py - contains a list of account dicts

# FLASK magic
from flask import Flask
from flask import request
from flask import abort

app = Flask(__name__)


@app.route('/debug')
def debug():
    """Ensure server works"""
    raise Exception


@app.route('/_weasyl_disco/api/v1.0/allocate_key', methods = ["GET"])
def allocate_key():
    """Allocate a Weasyl API key"""
    global WEASYL_LOGIN_DETAILS# I don't know why but we need this here
    # Get a API key
    # Sort the list by last used
    WEASYL_LOGIN_DETAILS = sorted(WEASYL_LOGIN_DETAILS, key=lambda k: k['last_used'])# http://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
    for account in WEASYL_LOGIN_DETAILS:
        if not account['allocated']:
            account['last_used'] = time.time()
            account['allocated'] = True
            api_key = account['api_key']
            print("Key allocated: %s" % (api_key))
            login_data = {'api_key':api_key, 'success':True}
            json_to_send = json.dumps(login_data)
            return json_to_send
    print('Cannot allocate key.')
    return json.dumps({'success':False})


@app.route('/_weasyl_disco/api/v1.0/deallocate_key', methods = ["POST"])
def deallocate_key():
    """Deallocate a Weasyl API key"""
    global WEASYL_LOGIN_DETAILS# I don't know why but we need this here
    if not request.json or not 'api_key' in request.json:
        print('Recieved bad request trying to deallocate key.')
        print(request)
        abort(400)
    api_key = request.json['api_key']

    for account in WEASYL_LOGIN_DETAILS:
        if account['api_key'] == api_key:
            account['allocated'] = False
            print("Key Deallocated: %s" % (api_key))
            return json.dumps({'success':True})
    return json.dumps({'success':False})


def main():
    try:
        logging.basicConfig(level=logging.DEBUG)
        app.debug = True
        app.run(host='0.0.0.0')# Let anyone anywhere access this, easier to be insecure.
    except Exception, e:# Log fatal exceptions
        logging.critical('Unhandled exception!')
        logging.exception(e)
    return


if __name__ == '__main__':
    main()
