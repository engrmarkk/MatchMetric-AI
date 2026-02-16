from api_services.const_response import return_response
from api_services.status_messages import StatusResponse as Res
from rest_framework.views import APIView
import rest_framework.status as http_status


class PingView(APIView):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        return return_response(Res.SUCCESS, http_status.HTTP_200_OK, "Pong")
