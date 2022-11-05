from rest_framework.exceptions import APIException
from rest_framework.views import status


class RedundantDeleteError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Department is already inactive"


class RedundantActivateError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Department is already active"
