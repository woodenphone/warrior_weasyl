Tested in the archiveteam-dev-env, unsupported elsewhere.

Intended to back up weasyl.com
API keys from properly-configured accounts will be required to use this.
To prepare a new account:
    Generate a new email account
    Fill in login form with an age over 22
    Open link in confirmation email

    Open "Site preferences" https://www.weasyl.com/control/editpreferences
    Set timezone to UTC+0 (ICELAND) ?Atlantic/Reykjavik?
    Set "Maximum Viewable Content Rating" to "Explicit"
    Set  "Maximum Viewable Content Rating in SFW Mode" to "Explicit"
    Click "Save"

    Add an API key - https://www.weasyl.com/control/apikeys
    ("warrior" as key description is fine)
    Click new API key
    Copy the new key 
    

Youtube embed submissions will probably not have the video saved.
TODO: verify google docs embed submissions are saved

Don't make the ranges too big.
Maybe around 100 or 1000 ids per job?
Jobs are given through archiveteam tracker thingy

Command to run:
run-pipeline pipeline.py YOURNICKHERE


Modes:
submission:<LOW>-<HIGH>
character:<LOW>-<HIGH>
journal:<LOW>-<HIGH>
TODO:user:userID


License:
I don't know, i just make things.