from rest_framework.response import Response
from rest_framework.exceptions import APIException


def rethink():
    from django.conf import settings
    import rethinkdb
    rethinkdb.connect(settings.RETHINK_HOST, settings.RETHINK_PORT, settings.RETHINK_DB)
    return rethinkdb

def error_response(s, e, status=400):
    return Response({'errors': s.errors, 'offender': e}, status=status)

def check(res):
    if res['errors']:
        print 'errors:', res
        e = APIException()
        e.status_code = 500
        e.detail = "Internal Error"
        raise e
    return res