#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import io
import json

AUTHOR = ''
SITENAME = 'New Salem - Pelican'
SITEURL = ''
THEME = "./pelican-twitchy"

PATH = 'content'
TAG_NAMES = json.load(open("tags.json"))
CAT_NAMES = {"swp":"Salem Witchcraft Papers", "salvrec":"Salem Village Records"}
CAT_SORT = {"swp":"SLUG", "salvrec":"DATE"}

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

TIMEZONE = 'EST'
ARTICLE_ORDER_BY = 'basename'
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
