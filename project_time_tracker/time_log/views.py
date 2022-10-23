from rest_framework.response import Response
from rest_framework.views import APIView

from .crud import TimeLogCRUD
from .models import TimeLog
from .serializers import TimeLogSerializer

timelog_crud = TimeLogCRUD(model=TimeLog)


class TimeLogListCreateApi(APIView):

    def get(self, request):
        time_logs = timelog_crud.get_all()
        data = TimeLogSerializer(time_logs, many=True).data
        return Response(data)


class TimeLogRetrieveUpdateDelete(APIView):

    def get(self, request, item_id: int):
        obj = timelog_crud.get_by(pk=item_id)
        data = TimeLogSerializer(obj).data
        return Response(data)
