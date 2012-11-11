import datetime
import uuid
from django.dispatch import Signal
from rest_framework import serializers
from beaver.fields import DictField
from beaver.utils import simplify
from beaver.utils import mkutime, utctime

message_received = Signal(providing_args=['message'])


class LogEntrySerializer(serializers.Serializer):
    id      = serializers.CharField(required=False)
    user    = serializers.CharField()
    message = serializers.CharField()
    created = serializers.DateTimeField(required=False)
    level   = serializers.CharField(required=False)
    logger  = serializers.CharField(required=False)
    meta    = DictField(required=False)
    timestamp = serializers.FloatField(required=False)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.user    = attrs['user']
            instance.created = attrs['created']
            instance.message = attrs['message']
            instance.level   = attrs['level']
            instance.logger  = attrs['logger']
            instance.meta    = attrs['meta']
            instance.timestamp = attrs['timestamp']
            instance.id = attrs['id']
            return instance

        ret = LogEntry(**attrs)
        message_received.send(LogEntry, message=ret)
        return ret

    def save(self, r):
        return r.table('log_entries').insert(simplify(self.data)).run()


class LogEntry(object):
    def __init__(self, user=None, created=None, timestamp=None, message=None, level='INFO', logger='default', meta=None):
        self.user = user
        if not timestamp:
            if created:
                self.timestamp = mkutime(created)
            else:
                self.timestamp = utctime()
        else:
            self.timestamp = timestamp
        if not created:
            self.created = datetime.datetime.utcfromtimestamp(self.timestamp)
        else:
            self.created = created
        self.message = message
        self.id = str(uuid.uuid1())
        self.level = level
        self.logger = logger
        self.meta = meta or {}