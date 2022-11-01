from rest_framework.exceptions import APIException
from rest_framework.views import status

class RedundantUserDeleteError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "User is already inactive"

class RedundantUserActivateError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "User is already active"