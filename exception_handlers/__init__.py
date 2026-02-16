from rest_framework.views import exception_handler
from api_services.status_messages import StatusResponse as Res
from api_services.const_response import return_response


def custom_exception_handler(exc, context):
    # Get the default response from DRF
    response = exception_handler(exc, context)

    if response is not None:
        # Replace DRF's default format with my own
        return return_response(
            Res.FAILED,
            status=response.status_code,
            message=response.data.get("detail", "Something went wrong"),
        )

    return response
