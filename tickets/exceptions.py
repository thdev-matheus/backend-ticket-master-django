from rest_framework.exceptions import APIException
from rest_framework.views import status

class RedundantSolveError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Ticket is already closed (solved)"