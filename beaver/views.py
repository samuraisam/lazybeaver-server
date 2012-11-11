from rest_framework.response import Response
from rest_framework.views import APIView
from beaver.models.log_entry import LogEntrySerializer
from beaver.utils import utctime
from beaver.models import rethink, check, error_response


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


class BuiltinReports:
    @staticmethod
    def active_sessions(r, request):
        now = utctime()
        cutoff = float(request.GET.get('cutoff', '5'))
        then = now - cutoff

        return r.table('log_entries').filter(
            lambda e: (e['message'] == 'session start') | (e['message'] == 'session end')
        ).run()


class ReportsBuiltin(APIView):
    def get(self, request, name=None, format=None):
        r = rethink()
        return
