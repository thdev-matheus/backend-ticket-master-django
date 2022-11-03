from rest_framework.exceptions import APIException
from rest_framework.views import status

class UnauthorizedUserCreateSolutionError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "You need to be the user solving the ticket or that opened the ticket to explain the ticket's solution"

class UnauthorizedUserListAllSolutionsError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "You need to be an admin to access all solutions of all tickets"

class UnauthorizedUserListSolutionError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "You need to be an admin, a member of the department or who created the associated ticket to access a solution"

class UnauthorizedUserListSolutionError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "You need to be an admin or a member of the department to view all open tickets"