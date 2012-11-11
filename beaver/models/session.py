import uuid
from rest_framework import serializers
from django.dispatch import receiver
from beaver.utils import simplify
from beaver.models import rethink, check
from beaver.models.log_entry import message_received


class SessionSerializer(serializers.Serializer):
    id = serializers.CharField()
    start_time = serializers.FloatField()
    end_time = serializers.FloatField(required=False)
    user = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.user = attrs['user']
            instance.start_time = attrs['start_time']
            instance.end_time = attrs['end_time']
            return instance
        ret = Session(**attrs)
        return ret

    def insert(self, r):
        return r.table('sessions').insert(simplify(self.data)).run()

    def update(self, r):
        return r.table('sessions').get(self.object.id).update(simplify(self.data)).run()


class Session(object):
    def __init__(self, id=None, start_time=None, end_time=None, user=None):
        if not id:
            self.id = str(uuid.uuid1())
        else:
            self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.user = user


@receiver(message_received)
def on_got_message(sender, message=None, **kwargs):
    if message.message in ('session start', 'session end'):
        r = rethink()
        new = False
        if message.message == 'session start':
            d = {}
            d['id'] = message.id
            d['start_time'] = message.timestamp
            d['user'] = message.user
            new = True
        else:
            # find the existing session to close
            d = list(r.table('sessions').filter(
                lambda e: e['user'] == message.user
            ).order_by('start_time').limit(1).run())[0]
            d['end_time'] = message.timestamp
        s = SessionSerializer(data=d)
        if new:
            check(s.insert(r))
        else:
            check(s.update(r))
