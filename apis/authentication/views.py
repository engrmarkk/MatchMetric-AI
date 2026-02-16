from rest_framework.views import APIView
from api_services.const_response import return_response
import rest_framework.status as http_status
from api_services.status_messages import StatusResponse as Res
from api_services.utils import (
    get_tokens_for_user,
    validate_email,
    validate_password,
    validate_not_more_than_two_words,
)
from db_cruds import create_user, email_exists
from django.contrib.auth import authenticate
from rest_framework.response import Response


# login view
class LoginView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request) -> Response:
        data = request.data
        email: str = data.get("email")
        password: str = data.get("password")
        is_valid = validate_email(email)
        if is_valid:
            return return_response(
                Res.FAILED, http_status.HTTP_400_BAD_REQUEST, is_valid
            )
        user = authenticate(email=email, password=password)
        if user is None:
            return return_response(
                Res.FAILED, http_status.HTTP_400_BAD_REQUEST, "Invalid credentials"
            )
        token_dict = get_tokens_for_user(user)
        return return_response(
            Res.SUCCESS, http_status.HTTP_200_OK, "Login successful", token_dict
        )


# register view
class RegisterView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        data = request.data
        first_name: str = data.get("first_name")
        last_name: str = data.get("last_name")
        email: str = data.get("email")
        password: str = data.get("password")
        if not first_name or not last_name:
            return return_response(
                Res.FAILED,
                http_status.HTTP_400_BAD_REQUEST,
                "First name and last name are required",
            )
        if validate_not_more_than_two_words(
            first_name
        ) or validate_not_more_than_two_words(last_name):
            return return_response(
                Res.FAILED,
                http_status.HTTP_400_BAD_REQUEST,
                "First name and last name must not contain more than two words",
            )
        is_email_valid = validate_email(email)
        if is_email_valid:
            return return_response(
                Res.FAILED, http_status.HTTP_400_BAD_REQUEST, is_email_valid
            )
        is_pass_valid = validate_password(password)
        if is_pass_valid:
            return return_response(
                Res.FAILED, http_status.HTTP_400_BAD_REQUEST, is_pass_valid
            )

        if email_exists(email.strip()):
            return return_response(
                Res.FAILED, http_status.HTTP_400_BAD_REQUEST, "Email already exists"
            )

        create_user(first_name, last_name, email, password)

        return return_response(
            Res.SUCCESS, http_status.HTTP_201_CREATED, "Registration successful"
        )
