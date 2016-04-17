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
import os

wpull_hook = globals().get('wpull_hook')  # silence code checkers


ITEM_NAME = os.environ['item_name']
WEASYL_MODE = ITEM_NAME.split(':')[0]
WEASYL_RANGE = ITEM_NAME.split(':')[1]


def accept_submission_page(url_info, record_info, verdict, reasons):
    """Determine whether to accept a submission page"""
    assert('weasyl.com/submission/' in url)
    print('Processing submission page link. url: %s' % (url))

    # Accept tag history links - https://www.weasyl.com/submission/tag-history/1236068
    if ( ('weasyl.com' in url) and ('/tag-history/' in url) ):
        print('Accept tag history links. url: %s' % (url))
        return True

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
        (referrer_submission_id not in url)# If previously on a submission, this will be the submissionID of that submission
        ):
        print('Ignoring submission for url: %s with refferer of %s\r\n' % (url, record_info['referrer']))
        return False
    else:
        print('Accept submission page. url: %s' % (url))
        return True


def accept_character_page(url_info, record_info, verdict, reasons):
    """Determine whether to accept a character page"""
    assert('weasyl.com/character/' in url)
    print('Processing character page link. url: %s' % (url))

    if (record_info['level'] <= 1):# If this is the command line args or redirected from them
        return True
    return False


def accept_journal_page(url_info, record_info, verdict, reasons):
    """Determine whether to accept a journal page"""
    assert('weasyl.com/journal/' in url)
    print('Processing journal page link. url: %s' % (url))

    if (record_info['level'] <= 1):# If this is the command line args or redirected from them
        return True
    return False



def accept_url(url_info, record_info, verdict, reasons):
    url = url_info['url']
    #print('processing url: %s with record_info of %s' % (url, record_info))
    # Always accept things given through command line arguments
    if record_info['referrer'] is None:
        print('Accept command-line specified URLs. url: %s \r\n' % (url))
        return True



    if ( ('weasyl.com/submission/' in url) and (WEASYL_MODE == 'submission') ):# Submission pages
        return accept_submission_page(url_info, record_info, verdict, reasons)

    if ( ('weasyl.com/character/' in url) and (WEASYL_MODE == 'character') ):# character pages
        return accept_character_page(url_info, record_info, verdict, reasons)

    if ( ('weasyl.com/journal/' in url) and (WEASYL_MODE == 'journal') ):# journal pages
        return accept_journal_page(url_info, record_info, verdict, reasons)


    if (WEASYL_MODE == 'user'):# User mode
         # Accept Submission galleries pages
        # https://www.weasyl.com/submissions?userid=3058&folderid=4329
        if ( ('weasyl.com/submissions' in url) and
        ('weasyl.com/submissions' in record_info['referrer']) and
        (not url.endswith('weasyl.com/submissions')) and
        (not url.endswith('weasyl.com/submissions/'))
        ):
            print('Accept submissions gallery listing pages. url: %s' % (url))
            return True

        # Accept characters galleries pages
        if ( ('weasyl.com/characters' in url) and
        ('weasyl.com/characters' in record_info['referrer']) and
        (not url.endswith('weasyl.com/characters')) and
        (not url.endswith('weasyl.com/characters/'))
        ):
            print('Accept characters gallery listing pages. url: %s' % (url))
            return True

        # Accept favorites galleries pages
        if ( ('weasyl.com/favorites' in url) and
        ('weasyl.com/favorites' in record_info['referrer']) and
        (not url.endswith('weasyl.com/favorites')) and
        (not url.endswith('weasyl.com/favorites/'))
        ):
            print('Accept favorites gallery listing pages. url: %s' % (url))
            return True

        # Accept journals listing pages
        if ( ('weasyl.com/journals' in url) and
            ('weasyl.com/journals' in record_info['referrer']) and
            (not url.endswith('weasyl.com/journals')) and
            (not url.endswith('weasyl.com/journals/'))
            ):
            print('Accept journals listing pages. url: %s' % (url))
            return True


        # Accept Followed By listing pages
        if ( ('weasyl.com/followed' in url) and
            ('weasyl.com/followed' in record_info['referrer']) and
            (not url.endswith('weasyl.com/followed')) and
            (not url.endswith('weasyl.com/followed/'))
             ):
            print('Accept Followed By listing pages. url: %s' % (url))
            return True

        # Accept Following listing pages
        if (
            ('weasyl.com/following' in url) and
            (not url.endswith('weasyl.com/following')) and
            (not url.endswith('weasyl.com/following/')) and
            ('weasyl.com/following' in record_info['referrer'])
            ):
            print('Accept Following listing pages. url: %s' % (url))
            return True

        # Accept friends listing pages
        if (
            ('weasyl.com/friends' in url) and
            (not url.endswith('weasyl.com/friends')) and
            (not url.endswith('weasyl.com/friends/')) and
            ('weasyl.com/friends' in record_info['referrer'])
            ):
            print('Accept friends listing pages. url: %s' % (url))
            return True

        # Accept shouts listing pages
        if (
            ('weasyl.com/shouts' in url) and
            (not url.endswith('weasyl.com/shouts')) and
            (not url.endswith('weasyl.com/shouts/')) and
            ('weasyl.com/shouts' in record_info['referrer'])
            ):
            print('Accept shouts listing pages. url: %s' % (url))
            return True

        # Accept collections pages
        if (
            ('weasyl.com/collections' in url) and
            (not url.endswith('weasyl.com/collections')) and
            (not url.endswith('weasyl.com/collections/')) and
            ('weasyl.com/collections' in record_info['referrer'])
            ):
            print('Accept collections listing pages. url: %s' % (url))
            return True

        # Reject usepages other than ones we input through user:USERID mode
        if ( ('weasyl.com/~' in url) and (WEASYL_RANGE not in url) ):
            #print('Reject non-specified userpage %s' % (url))
            return False

    # Accept submission download links (This includes the download links for text submissions)
    # https://cdn.weasyl.com/~hattonslayden/submissions/1241567/af1c9582c794e97a166afc1a646d222645db57bbad3cb161f95c61e5e41a59ae/hattonslayden-intergalactic-vixen-around-the-bend.jpg?download
    if ( ('cdn.weasyl.com/~' in url) and ('/submissions/' in url) and (url.endswith('?download')) ):
        print('Accept submission download links. url: %s' % (url))
        return True

##    # Rejections
##    # Reject unwanted domains
##    if 'google-analytics.com' in url:
##        return False
##    if 'google.com/analytics' in url:
##        return False
##    if 'gstatic.com/analytics' in url:
##        return False
##    if 'googleadservices.com' in url:
##        return False
##    if 'googlesyndication.com/pagead/' in url:
##        return False
##    if 'googletagservices.com' in url:
##        return False
##    if '2mdn.net' in url:
##        return False
##    if 'ytimg.com' in url:
##        return False
##    if 'google.com/images' in url:
##        return False
##    if 'gstatic.com/' in url:
##        return False
##    if 'fonts.gstatic.com/' in url:# Maybe we need this?
##        return False
##    if 'ajax.googleapis.com/' in url:# Maybe we need this?
##        return False
##    if 'doubleclick.net/' in url:# Ads
##        return False
##
##    # Reject weasyl things we don't want to load
##    if 'weasyl.com/search' in url:
##        return False
##    if 'weasyl.com/help' in url:
##        return False
##    if 'weasyl.com/notes' in url:
##        return False
##    if 'weasyl.com/frienduser' in url:
##        return False
##    if 'weasyl.com/policy' in url:
##        return False
##    if 'weasyl.com/ignoreuser' in url:
##        return False
##    if 'weasyl.com/submit' in url:
##        return False
##    if 'weasyl.com/signout' in url:
##        return False
##    if 'weasyl.com/staff' in url:
##        return False
##    if 'weasyl.com/control' in url:# https://www.weasyl.com/control
##        return False
##    if 'weasyl.com/followuser' in url:
##        return False
##    if 'weasyl.com/index' in url:
##        return False
##    if 'weasyl.com/thanks' in url:
##        return False
##    if 'weasyl.com/remove' in url:# https://www.weasyl.com/remove/comment
##        return False
##    if 'weasyl.com/favorite' in url:# https://www.weasyl.com/favorite
##        return False
##    if 'weasyl.com/static/images/' in url:# Site layout images, these can be grabbed seperately
##        return False
##    if 'weasyl.com/api/' in url:# 404 but somewhow gets linked to
##        return False
##    if url.endswith('weasyl.com'):
##        return False

    # Reject static site elements so we don't get a thousand copies of the title header image
    # https://cdn.weasyl.com/static/images/logo.png
    if 'https://cdn.weasyl.com/static/images/' in url:
        return False

    # Acceptions
    # Accept thumbnails
    # https://cdn.weasyl.com/static/media/3b/21/a1/3b21a1948998be341205950d97e154e8218ecbbb4e563353b80cdf278639e3c8.jpg
    if ( ('weasyl.com/static/media/' in url) ):
        return False# TODO REMOVEME (temporary override to speed up testing)
        return True

    # ===Submission, character, journal display pages===

    # Accept character download links
    # https://cdn.weasyl.com/static/character/4e/7a/2d/c2/35/e5/beaniee-61364.submit.41340.png
    if ( ('cdn.weasyl.com/static/character' in url) and ('weasyl.com/character/' in record_info['referrer']) ):
        print('Accept character download links. url: %s' % (url))
        return True

    # Accept text submission images and thumbnails. Restrict to submission pages to try to reduce bloat
    # https://cdn.weasyl.com/static/media/37/6a/c2/376ac29cf432b843009c9bc18682fbef1db9282dbd77f4c311a598224b222807.jpg
    if ( ('cdn.weasyl.com/static/media' in url) and ('weasyl.com/submission/' in record_info['referrer']) ):
        print('Accept text submission images and thumbnails. url: %s' % (url))
        return False# TODO REMOVEME (temporary override to speed up testing)
        return True

    # Accept google docs embeds
    # https://docs.google.com/document/d/1pSeP8GdGA7FMGv5sXk97NiBPkUPZwj8jNT_7MiHriWY/edit?usp=sharing
    # TODO

##    if verdict:
##        print('Using defualt verdict of %s for url: %s with record_info of %s' % (verdict, url, record_info))
##    return verdict
    if verdict:
        print('Ignoring defualt verdict of %s for url: %s with refferer of %s' % (verdict, url, record_info['referrer']))
    return False


















wpull_hook.callbacks.accept_url = accept_url
wpull_hook.callbacks.version = 3