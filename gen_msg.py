import argparse
import requests
import datetime
import json

parser = argparse.ArgumentParser(description='Send a log message')
parser.add_argument('--host', default='http://localhost:8000', help='The host, including scheme and port, without path')
parser.add_argument('--message', type=str)

def do_send(host, message):
    j = json.dumps(
        {
            'entries': [
                {
                    'message': message,
                    'created': datetime.datetime.utcnow().isoformat(),
                    'logger': 'test',
                    'level': 'INFO',
                    'user': 'none'
                }
            ]
        }
    )
    r = json.loads(requests.post('{}/api/logs'.format(host), data=j,
                   headers={'content-type': 'application/json'}).content)
    print json.dumps(r, indent=4)

if __name__ == '__main__':
    args = parser.parse_args()
    do_send(args.host, args.message)
