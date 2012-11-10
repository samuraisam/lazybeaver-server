lazybeaver-server
=================

Collects fairly arbitrary log data. Does absolutely nothing else, yet.

API:
----

The API is described thusly:

POST  `/logs`
-------------

Create a series of new log entries.

*Format Expected*

    {
        'entries': [
            {
                'message': 'Arbitrarily long message',
                'user': 'usertag',
                'created': 'ISO 8601 Date',
                'level': 'LOG_LEVEL',
                'logger': 'myloger',
                'meta': {
                    'arbitrary': 'keys and values'
                }
            }
        ]
    }

*Format Returned*

    {
        "entries": [
            {
                "id": "105e2d40-2b74-11e2-9551-000c29966c46",
                "user": "ssutch",
                "message": "hello der",
                "created": "2012-11-10T20:20:26.530",
                "level": "WARNING",
                "logger": "not_default",
                "meta": {
                    "shits": "and giggles"
                }
            }
        ]
    }

*Optional Fields*

    * `logger` default is "default"
    * `level` default is "INFO"
    * `meta` will default to empty dictionary
    * `created` will default to the current time in UTC
