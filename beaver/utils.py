import calendar
import datetime
from rest_framework.utils.encoders import JSONEncoder

def mkutime(d):
    return float(calendar.timegm(d.timetuple())) + float(d.microsecond) / 1e6


def utctime():
    """
    Generate a timestamp from the current time in UTC
    """
    d = datetime.datetime.utcnow()
    return mkutime(d)

enc = JSONEncoder()

def simplify(d):
    t, d = seq_or_no_seq(d)
    if t == dict:
        return {seq_or_no_seq(k)[1]: simplify(v) for k, v in d.iteritems()}
    elif t == list:
        return [simplify(v) for v in d]
    return d


def seq_or_no_seq(v):
    if isinstance(v, dict):
        return dict, v
    elif isinstance(v, (set, frozenset, list)) or hasattr(v, '__iter__'):
        return list, list(v)
    elif isinstance(v, basestring):
        if isinstance(v, unicode):
            return str, v.encode('utf8')
        return str, v
    elif isinstance(v, (int, long, float)):
        return int, v
    elif v == None:
        return None, None
    return str, enc.default(v)