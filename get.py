#!/usr/bin/env python

import logging
from optparse import OptionParser
import sys

import requests


def simplerepr(obj):
    keys = sorted(key for key in obj.__dict__.keys() if not key.startswith('_'))
    attrs = ''.join(' %s=%r' % (key, obj.__dict__[key]) for key in keys)
    return '<%s%s>' % (obj.__class__.__name__, attrs)



class Item(object):

    def __init__(self, item_json):
        self.id = item_json['id']
        if 'geocode' in item_json:
            self.geocode = map(float, item_json['geocode'].split())
        else:
            self.geocode = None

    __repr__ = simplerepr


def main(argv):
    option_parser = OptionParser()
    option_parser.add_option('-c', '--create-table', action='store_true')
    option_parser.add_option('-t', '--table', default='devfestzurich', metavar='TABLE')
    option_parser.add_option('-q', '--query', metavar='QUERY')
    option_parser.add_option('-k', '--key', default='AIzaSyBfoMH8qNEQYBjLA9u0jLgs5V6o7KiAFbQ', metavar='KEY')
    option_parser.add_option('-l', '--limit', default=20, metavar='LIMIT', type=int)
    option_parser.add_option('-f', '--fields', default='items(geocode,id),nextPageToken', metavar='FIELDS')
    options, args = option_parser.parse_args(argv[1:])

    logging.basicConfig(level=logging.INFO)

    params = {
        'fields': options.fields,
        'key': options.key,
        'maxResults': 20,
        'query': options.query,
        }
    results = []
    while len(results) < options.limit:
        response = requests.get('https://www.googleapis.com/plus/v1/activities', params=params)
        logging.info('got %d items, %d with geocode' % (len(response.json['items']), len([item for item in response.json['items'] if 'geocode' in item])))
        for item_json in response.json['items']:
            if 'geocode' in item_json:
                results.append(Item(item_json))
        if 'nextPageToken' in response.json:
            params['pageToken'] = response.json['nextPageToken']
        else:
            break

    print repr(results)



if __name__ == '__main__':
    sys.exit(main(sys.argv))
    