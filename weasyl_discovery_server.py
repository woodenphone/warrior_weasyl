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





@app.route('/')
def hello():
    """Ensure server works"""
    return 'Furaffinity disco server running.\r\n'


@app.route('/debug')
def debug():
    """Ensure server works"""
    raise Exception


@app.route('/_weasyl_disco/api/get_secrets', methods = ["POST", "GET"])
def serve_weasyl_logins():
    """Serve FA passwords"""
    global WEASYL_LOGIN_DETAILS# I don't know why but we need this here
    # Get a username/password pair
    # Sort the list by last used
    WEASYL_LOGIN_DETAILS = sorted(WEASYL_LOGIN_DETAILS, key=lambda k: k['last_used'])# http://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
    account = WEASYL_LOGIN_DETAILS[0]
    account['last_used'] = time.time()
    # TODO: Disable sending out a username for x time after it was last used
    # Encode the login details
    login_data = {
        'api_key':account['api_key'],
        }

    json_to_send = json.dumps(login_data)
    return json_to_send




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
