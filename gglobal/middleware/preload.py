#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import codecs
from django.conf import settings
from django.utils.html_parser import HTMLParser

__author__ = 'Paweł Krawczyk'


class ResourceFinder(HTMLParser):
    resources = {}

    def handle_starttag(self, tag, attrs):
        res_type = None
        res_uri = None
        res_op = 'prefetch'

        if tag == 'link':
            for attr in attrs:
                if attr[0] == 'rel' and attr[1] == 'stylesheet':
                    res_type = 'style'
                if attr[0] == 'href' and len(attr[1]):
                    res_uri = attr[1]

        if tag == 'script':
            res_type = 'script'
            for attr in attrs:
                if attr[0] == 'src' and len(attr[1]):
                    res_uri = attr[1]

        if tag in ('img', 'picture'):
            res_type = 'image'
            for attr in attrs:
                if attr[0] == 'src' and len(attr[1]):
                    res_uri = attr[1]

        if tag in ('audio', 'video'):
            res_type = 'media'
            for attr in attrs:
                if attr[0] == 'src' and len(attr[1]):
                    res_uri = attr[1]

        if tag in ('frame', 'iframe'):
            res_type = 'document'
            res_op = 'prerender'
            for attr in attrs:
                if attr[0] == 'src' and len(attr[1]):
                    res_uri = attr[1]

        if tag == 'embed':
            res_type = 'embed'
            for attr in attrs:
                if attr[0] == 'src' and len(attr[1]):
                    res_uri = attr[1]

        if tag == 'object':
            res_type = 'object'
            for attr in attrs:
                if attr[0] == 'src' and len(attr[1]):
                    res_uri = attr[1]

        # update the list of resources
        if res_type and res_uri:
            # add the rel=preload as=type record
            self.resources[res_uri] = {'rel': res_op, 'as': res_type}

            # add DNS prefetch record
            o = urlparse(res_uri)
            if hasattr(o, 'hostname'):
                self.resources['//{}'.format(o.hostname)] = {'rel': 'dns-prefetch'}


class ResourceHintsMiddleware(object):
    """
    Adds Link resource hints header to responses to hint browser which resources can be prefetched to speed up
    loading of the page. The list of resources to preload is built automatically based on each response body,
    which is scanned for supported resource types. These resources are added as 'prefetch' resources hints
    rather than 'preload' which has much higher priority and may be better suited for manual fine-tuning
    Resources can be also manually added (or overriden) using PRELOAD_RESOURCES configuration variable
    in Django settings. At least the 'rel' specification is required for each resource:
        PRELOAD_RESOURCES = {
        # https://w3c.github.io/resource-hints/
        '//cdnjs.cloudflare.com': {'rel': 'dns-prefetch' },
        '/next.html': {'rel': 'prefetch', 'as': 'html', 'crossorigin': 'use-credentials' },
        '/ads.html': {'rel': 'prerender' },
        # https://w3c.github.io/preload/
        '/style.css': {'rel': 'preload', 'as': 'style' },
        '/font.woff': {'rel': 'preload', 'as':' font', 'crossorigin': True },
        }
    Sample output:
    Link: <//webcookies-20c4.kxcdn.com/no_photo_small.gif>; as=image; rel=prefetch,
          <//cdnjs.cloudflare.com>; rel=dns-prefetch
    Usage:
    
    1. Create a `middleware' module in your Django project directory and place `preload.py' inside
    2. Edit your `settings.py`:
    MIDDLEWARE = [
    ...
    'middleware.preload.ResourceHintsMiddleware',
    ...
    ]
    References:
        * https://w3c.github.io/preload/
        * https://w3c.github.io/resource-hints/
        * https://tools.ietf.org/html/rfc5988
    """
    parser = ResourceFinder()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        links = []

        response = self.get_response(request)

        # returning Link header for any other content than HTML doesn't make sense
        if response.get('Content-Type', '').startswith('text/html'):

            # preserve existing Link headers
            if 'Link' in response:
                links = response['Link'].split(',')

            # parse the response body and return dictionary of preloadable resources
            try:
                body = codecs.decode(response.content, response.charset)
                self.parser.reset()
                self.parser.feed(body)
                final_resources = self.parser.resources
            except UnicodeDecodeError as e:
                # fail safe in case of weird encodings
                final_resources = {}

            # overwrite automatically collected resources with manually configured ones
            if hasattr(settings, 'PRELOAD_RESOURCES'):
                for res, conf in settings.PRELOAD_RESOURCES.items():
                    final_resources[res] = conf

            # produce the Link header from merged automatic and manual resources
            for res, conf in final_resources.items():
                link = "<{}>".format(res)
                for k, v in conf.items():
                    link += "; {}={}".format(k, v)
                links.append(link)

            response['Link'] = ', '.join(links)

        return response