from rest_framework.exceptions import APIException
from rest_framework.views import status


class RedundantSolveError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Ticket is already closed (solved)"


class NoTicketsError(APIException):
    status_code = status.HTTP_200_OK
    default_detail = "User never opened a ticket"


class NoTicketsToSolveError(APIException):
    status_code = status.HTTP_200_OK
    default_detail = "You are not assigned to any opened ticket"


class UnathorizedListingError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "To view all tickets from or assigned to an user, you must be the user or an Admin"
