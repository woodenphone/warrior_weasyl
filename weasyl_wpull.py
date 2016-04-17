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
    print('processing url: %s with record_info of %s' % (url, record_info))
    # Always accept things given through command line arguments
    if record_info['referrer'] is None:
        print('Accept command-line specified URLs. url: %s \r\n' % (url))
        return True

    # Rejections
    if verdict:
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
        if 'fonts.gstatic.com/' in url:# Maybe we need this?
            return False
        if 'ajax.googleapis.com/' in url:# Maybe we need this?
            return False
        if 'doubleclick.net/' in url:# Ads
            return False

        # Reject weasyl things we don't want to load
        if 'weasyl.com/search' in url:
            return False
        if 'weasyl.com/help' in url:
            return False
        if 'weasyl.com/notes' in url:
            return False
        if 'weasyl.com/frienduser' in url:
            return False
        if 'weasyl.com/policy' in url:
            return False
        if 'weasyl.com/ignoreuser' in url:
            return False
        if 'weasyl.com/submit' in url:
            return False
        if 'weasyl.com/signout' in url:
            return False
        if 'weasyl.com/staff' in url:
            return False
        if 'weasyl.com/control' in url:# https://www.weasyl.com/control
            return False
        if 'weasyl.com/followuser' in url:
            return False
        if 'weasyl.com/index' in url:
            return False
        if 'weasyl.com/thanks' in url:
            return False
        if 'weasyl.com/remove' in url:# https://www.weasyl.com/remove/comment
            return False
        if 'weasyl.com/favorite' in url:# https://www.weasyl.com/favorite
            return False
        if 'weasyl.com/static/images/' in url:# Site layout images, these can be grabbed seperately
            return False
        if 'weasyl.com/api/' in url:# 404 but somewhow gets linked to
            return False
        if url.endswith('weasyl.com'):
            return False

        # Reject usepages other than ones we input through user:USERID mode
        if (
            ('weasyl.com/~' in url)
            ):
            return False

        # Reject links to submissions, unless they are linked to from the same submission or from the command line
        # ex "https://www.weasyl.com/submission/1221326" redirects to "https://www.weasyl.com/submission/1221326/two-big-cats"
        referrer_submission_id = None
        refferer_string = str(record_info['referrer'])
        referrer_submission_id_search = re.search('weasyl.com/submission/(\d+)', refferer_string)
        if referrer_submission_id_search:
            referrer_submission_id = referrer_submission_id_search.group(1)
        if (
            ('weasyl.com/submission/' in url) and
            (record_info['referrer'] is not None) and# Command-line specified submissions have referrer of None
            (referrer_submission_id is not None) and# If not previously on a submission, this will be None
            (referrer_submission_id not in url)# If previously on a submission, this will be the submissionID of that submission
            ):
            print('Ignoring submission for url: %s with refferer of %s\r\n' % (url, record_info['referrer']))
            return False

        # Reject static site elements so we don't get a thousand copies of the title header image
        # https://cdn.weasyl.com/static/images/logo.png
        if 'https://cdn.weasyl.com/static/images/' in url:
            return False

    # Acceptions
    else:
        # Accept thumbnails
        # https://cdn.weasyl.com/static/media/3b/21/a1/3b21a1948998be341205950d97e154e8218ecbbb4e563353b80cdf278639e3c8.jpg
        if (
            ('weasyl.com/static/media/' in url)
            ):
            return True

        # ===Submission, character, journal display pages===
        # Accept tag history links
        #
        if (
            ('weasyl.com' in url) and
            ('/tag-history/' in url)
            ):
            print('Accept tag history links. url: %s' % (url))
            return True

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

        # === USER ===
        # Accept Submission galleries pages
        # https://www.weasyl.com/submissions?userid=3058&folderid=4329
        if (
            (not verdict) and
            ('weasyl.com/submissions' in url) and
            ('weasyl.com/submissions' in record_info['referrer'])
            ):
            print('Accept submissions gallery listing pages. url: %s' % (url))
            return True

        # Accept characters galleries pages
        if (
            (not verdict) and
            ('weasyl.com/characters' in url) and
            ('weasyl.com/characters' in record_info['referrer'])
            ):
            print('Accept characters gallery listing pages. url: %s' % (url))
            return True

        # Accept favorites galleries pages
        if (
            (not verdict) and
            ('weasyl.com/favorites' in url) and
            ('weasyl.com/favorites' in record_info['referrer'])
            ):
            print('Accept favorites gallery listing pages. url: %s' % (url))
            return True

        # Accept journals By listing pages
        if (
            (not verdict) and
            ('weasyl.com/journals' in url) and
            ('weasyl.com/journals' in record_info['referrer'])
            ):
            print('Accept journals listing pages. url: %s' % (url))
            return True


        # Accept Followed By listing pages
        if (
            (not verdict) and
            ('weasyl.com/followed' in url) and
            ('weasyl.com/followed' in record_info['referrer'])
            ):
            print('Accept Followed By listing pages. url: %s' % (url))
            return True

        # Accept Following listing pages
        if (
            (not verdict) and
            ('weasyl.com/following' in url) and
            ('weasyl.com/following' in record_info['referrer'])
            ):
            print('Accept Following listing pages. url: %s' % (url))
            return True

        # Accept friends listing pages
        if (
            (not verdict) and
            ('weasyl.com/friends' in url) and
            ('weasyl.com/friends' in record_info['referrer'])
            ):
            print('Accept friends listing pages. url: %s' % (url))
            return True

        # Accept shouts listing pages
        if (
            (not verdict) and
            ('weasyl.com/shouts' in url) and
            ('weasyl.com/shouts' in record_info['referrer'])
            ):
            print('Accept shouts listing pages. url: %s' % (url))
            return True

        # Accept collections pages
        if (
            (not verdict) and
            ('weasyl.com/collections' in url) and
            ('weasyl.com/collections' in record_info['referrer'])
            ):
            print('Accept collections listing pages. url: %s' % (url))
            return True

    if verdict:
        print('Using defualt verdict of %s for url: %s with record_info of %s' % (verdict, url, record_info))
    return verdict
##    if verdict:
##        print('Ignoring defualt verdict of %s for url: %s with refferer of %s\r\n' % (verdict, url, record_info['referrer']))
##    return False


















wpull_hook.callbacks.accept_url = accept_url
wpull_hook.callbacks.version = 3