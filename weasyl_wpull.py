#-------------------------------------------------------------------------------
# Name:        wpull hooks for weasyl
# Purpose:
#
# Author:      User
#
# Created:     14/04/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import re


wpull_hook = globals().get('wpull_hook')  # silence code checkers






def accept_url(url_info, record_info, verdict, reasons):
    url = url_info['url']
    #print('processing url: %s' % (url))

    # Reject unwanted domains
    if 'google-analytics.com' in url:
        return False
    if 'google.com/analytics' in url:
        return False
    if 'gstatic.com/analytics' in url:
        return False
    if 'googleadservices.com' in url:
        return False
    if 'googlesyndication.com/pagead/' in url:
        return False
    if 'googletagservices.com' in url:
        return False
    if '2mdn.net' in url:
        return False
    if 'ytimg.com' in url:
        return False
    if 'google.com/images' in url:
        return False
    if 'gstatic.com/' in url:
        return False
    if 'fonts.gstatic.com/' in url:
        return False
    if 'ajax.googleapis.com/' in url:
        return False
    if 'doubleclick.net/' in url:
        return False


    # Reject static site elements so we don't get a thousand copies of the title header image
    # https://cdn.weasyl.com/static/images/logo.png
    if 'https://cdn.weasyl.com/static/images/' in url:
        return False

    # Accept submission download links (This includes the download links for text submissions)
    # https://cdn.weasyl.com/~hattonslayden/submissions/1241567/af1c9582c794e97a166afc1a646d222645db57bbad3cb161f95c61e5e41a59ae/hattonslayden-intergalactic-vixen-around-the-bend.jpg?download
    if (
        (not verdict) and
        ('cdn.weasyl.com/~' in url) and
        ('weasyl.com/submission/' in record_info['referrer']) and
        (url.endswith('?download'))
        ):
        print('Accept submission download links. url: %s' % (url))
        return True

    # Accept character download links
    # https://cdn.weasyl.com/static/character/4e/7a/2d/c2/35/e5/beaniee-61364.submit.41340.png
    if (
        (not verdict) and
        ('cdn.weasyl.com/static/character' in url) and
        ('weasyl.com/character/' in record_info['referrer']) and
        ('.submit.' in url)
        ):
        print('Accept character download links. url: %s' % (url))
        return True

    # Accept text submission images and thumbnails. Restrict to submission pages to try to reduce bloat
    # https://cdn.weasyl.com/static/media/37/6a/c2/376ac29cf432b843009c9bc18682fbef1db9282dbd77f4c311a598224b222807.jpg
    if (
        (not verdict) and
        ('cdn.weasyl.com/static/media' in url) and
        ('weasyl.com/submission/' in record_info['referrer'])
        ):
        print('Accept text submission images and thumbnails. url: %s' % (url))
        return True

    # Accept google docs embeds
    # https://docs.google.com/document/d/1pSeP8GdGA7FMGv5sXk97NiBPkUPZwj8jNT_7MiHriWY/edit?usp=sharing
    # TODO
    #print('using defualt verdict. url: %s' % (url))
    return verdict


















wpull_hook.callbacks.accept_url = accept_url
wpull_hook.callbacks.version = 3