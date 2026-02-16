from rest_framework.response import Response


def return_response(
    status_message: str, status: int, message: str, data=None, **kwargs
) -> Response:
    res = {
        "status": status_message,
        "message": message,
    }

    if data is not None:
        # If data is explicitly passed, put it under "data"
        res["data"] = data
    elif kwargs:
        # If kwargs are passed, unpack into root
        res.update(kwargs)

    return Response(res, status=status)
