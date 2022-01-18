import json
import time
import pprint
import argparse
import urllib.parse

import rich
import httpx

from . import logs

DEFAULT_URL = 'http://localhost:1337'

log = logs.get(__name__)

def command(url, **params):
    if params:
        request = httpx.post
        kwargs = {'json': params}
    else:
        request = httpx.get
        kwargs = {}

    res = request(url, **kwargs)

    if res.headers['content-type'] == 'application/json':
        data = res.json()
        if data:
            rich.print_json(data=data, sort_keys=True)
    else:
        print(res.text)

def events(url):
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
                        event['data'] = line[6:].strip()
                        log.info('event: %s', pprint.pformat(event))
                    else:
                        continue

        except (httpx.ConnectError, httpx.RemoteProtocolError) as e:
            log.warning('lost connection: %s', e)
            time.sleep(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', default=DEFAULT_URL,
        help='URL of the terracoder server (default: %(default)s)')
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help='enable verbose output (-vv for more)')
    parser.add_argument('command', nargs='?', help='the command to execute')
    parser.add_argument('parameters', nargs='*',
        help='parameters to pass to the command')

    args = parser.parse_args()
    logs.init(args.verbose)

    url = urllib.parse.urljoin(args.url, args.command or '')
    params = {k.strip(): json.loads(v.strip())
        for k, v in (p.split('=') for p in args.parameters)}

    if args.command == 'events':
        events(url)
    else:
        command(url, **params)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
