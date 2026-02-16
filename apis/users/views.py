from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from api_services.const_response import return_response
from api_services.status_messages import StatusResponse as Res
import rest_framework.status as http_status


# my profile
class MyProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def get(self, request) -> Response:
        user = request.user
        return return_response(
            Res.SUCCESS,
            http_status.HTTP_200_OK,
            "My profile",
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name.title(),
                "last_name": user.last_name.title(),
            },
        )
