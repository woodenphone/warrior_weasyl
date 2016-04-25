#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     20/04/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import requests
from bs4 import BeautifulSoup
import logins

def parse(submission_page_html):
    pass

def save_test_page():
    url = 'https://www.weasyl.com/submission/1245327/spooky-bandana'
    file_path = os.path.join( 'ignored', 'foo.html')
    headers = {'X-Weasyl-API-Key': logins.WEASYL_LOGIN_DETAILS[0]['api_key']}
    r = requests.get(url, headers=headers)
    with open(file_path, 'w') as f:
        f.write(r.content)

html_path = os.path.join( 'ignored', 'foo.html')
with open(html_path, 'r') as f:
    submission_page_html = f.read()
soup = BeautifulSoup(submission_page_html, 'html.parser')









def main():
    pass

if __name__ == '__main__':
    main()
