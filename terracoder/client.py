import os
import json
import time
import pprint
import argparse

import httpx

from .format import format
from . import output
from . import logs

DEFAULT_URL = 'http://localhost:1337'
RETRY_INTERVAL = 5

log = logs.get(__name__)

class Client:
    def __init__(self, url=None, *parts):
        self._url = os.path.join(url or DEFAULT_URL, *parts)

    def command(self, name=None, **params):
        if params:
            request = httpx.post
            kwargs = {'json': params}
        else:
            request = httpx.get
            kwargs = {}

        url = os.path.join(self._url, name or '')
        res = request(url, **kwargs)

        if res.headers['content-type'] == 'application/json':
            return res.json()
        else:
            return res.text

    def events(self):
        def gen(url):
            # let caller start the generator
            yield None

            while True:
                try:
                    log.info('connecting: %s ...', url)
                    with httpx.stream('GET', url, timeout=None) as res:
                        res.raise_for_status()

                        event = {}
                        for line in res.iter_lines():
                            if line.startswith('event:'):
                                event = {'name': line[7:].strip()}
                            elif line.startswith('data:'):
                                buf = line[6:].strip()
                                event['data'] = json.loads(buf)
                                yield event
                            else:
                                continue

                except (httpx.ConnectError, httpx.RemoteProtocolError) as e:
                    log.warning('lost connection: %s', e)
                finally:
                    time.sleep(RETRY_INTERVAL)

        url = os.path.join(self._url, 'events')
        return StreamInitiator(gen(url))

    def wait_for_event(self, events, event_name):
        for event in events:
            if event['name'] == event_name:
                return event

class StreamInitiator(object):
    """Captures the first value of a generator to ensure that it begins
    execution."""
    def __init__(self, gen):
        # start the generator
        next(gen)
        self._gen = gen

    def __iter__(self):
        for x in self._gen:
            yield x

def decode_value(v):
    try:
        return json.loads(v)
    except json.JSONDecodeError:
        return v

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', default=DEFAULT_URL,
        help='URL of the terracoder server (default: %(default)s)')
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help='enable verbose output (-vv for more)')
    parser.add_argument('command', nargs='?', help='the command to execute')
    parser.add_argument('parameters', nargs='*', metavar='<name>=<value>',
        help='parameters to pass to the command')

    args = parser.parse_args()
    logs.init(args.verbose)

    try:
        params = {k.strip(): decode_value(v.strip())
            for k, v in (p.split('=') for p in args.parameters)}
    except ValueError:
        parser.error('parameters must be in the format: <name>=<value>')

    client = Client(args.url)
    try:
        if args.command == 'events':
            for event in client.events():
                log.info('[event]\n%s', pprint.pformat(event))
        else:
            res = client.command(args.command, **params)
            if res:
                print(format(res))
                # func_name = args.command.replace('/', '_')
                # try:
                #     func = getattr(output, func_name)
                # except AttributeError:

                # else:
                #     print(func(res))
    except Exception as e:
        logger = log.exception if args.verbose > 0 else log.error
        logger('error: %s', e)
