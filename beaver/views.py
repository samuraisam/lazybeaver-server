import datetime
import uuid
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.utils.encoders import JSONEncoder

def rethink():
    from django.conf import settings
    import rethinkdb
    rethinkdb.connect(settings.RETHINK_HOST, settings.RETHINK_PORT, settings.RETHINK_DB)
    return rethinkdb

def error_response(s, e, status=400):
    return Response({'errors': s.errors, 'offender': e}, status=status)

def check(res):
    if res['errors']:
        e = APIException()
        e.status_code = 500
        e.detail = "Internal Error"
        raise e
    return res

enc = JSONEncoder()

def seq_or_no_seq(v):
    if isinstance(v, dict):
        return dict, v
    elif isinstance(v, (set, frozenset, list)) or hasattr(v, '__iter__'):
        return list, list(v)
    elif isinstance(v, basestring):
        if isinstance(v, unicode):
            return str, v.encode('utf8')
        return str, v
    return str, enc.default(v)

def simplify(d):
    t, d = seq_or_no_seq(d)
    if t == dict:
        return {seq_or_no_seq(k)[1]: simplify(v) for k, v in d.iteritems()}
    elif t == list:
        return [simplify(v) for v in d]
    return d

class LogEntry(object):
    def __init__(self, user=None, created=None, message=None, level='INFO', logger='default', meta=None):
        self.user = user
        self.created = created or datetime.datetime.utcnow()
        self.message = message
        self.id = str(uuid.uuid1())
        self.level = level
        self.logger = logger
        self.meta = meta or {}

class DictField(serializers.WritableField):
    type_name = 'DictField'

    default_error_messages = {
        'invalid': _("'%s' value must be a dict."),
    }

    def from_native(self, value):
        if value in validators.EMPTY_VALUES:
            return None

        try:
            return dict(value)
        except (TypeError, ValueError):
            msg = self.error_messages['invalid'] % value
            raise ValidationError(msg)

class LogEntrySerializer(serializers.Serializer):
    id      = serializers.CharField(required=False)
    user    = serializers.CharField()
    message = serializers.CharField()
    created = serializers.DateTimeField(required=False)
    level   = serializers.CharField(required=False)
    logger  = serializers.CharField(required=False)
    meta    = DictField(required=False)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.user    = attrs['user']
            instance.created = attrs['created']
            instance.message = attrs['message']
            instance.level   = attrs['level']
            instance.logger  = attrs['logger']
            instance.meta    = attrs['meta']
            return instance
        return LogEntry(**attrs)

    def save(self, r):
        return r.table('log_entries').insert(simplify(self.data)).run()

class LogEntryListSerializer(serializers.Serializer):
    entries = serializers.ManyRelatedField(LogEntrySerializer)

class Logs(APIView):
    def post(self, request, format=None):
        r = rethink()
        d = request.DATA
        serializers = []
        for entry in d['entries']:
            s = LogEntrySerializer(data=entry)
            if not s.is_valid():
                return error_response(s, entry)
            serializers.append(s)
            check(s.save(r))

        ret = {
            'entries': [s.data for s in serializers]
        }
        return Response(ret, status=201)

    def get(self, request, format=None):
        e = APIException()
        e.detail = "Farting"
        e.status_code = 400
        raise e
