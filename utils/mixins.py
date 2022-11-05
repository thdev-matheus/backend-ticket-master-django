import math
from tickets.models import Ticket

class SerializerMapping:
    serializer_map = None

    def get_serializer_class(self):
        return self.serializer_map.get(self.request.method)


def get_ticket_status(self, obj):
    status = ""
    if not obj.support:
        status = "Waiting"
    if obj.support and not obj.is_solved:
        status = "In progress"
    if obj.support and obj.is_solved:
        status = "Closed"
    return status

def solution_get_time_taken(self, obj):
    ticket = Ticket.objects.get(id=obj.ticket.id)
    time_to_solve = obj.solved_at - ticket.created_at
    days = math.floor(time_to_solve.seconds / 86400)
    hours = math.floor(time_to_solve.seconds % 86400 / 3600)
    minutes = math.floor(time_to_solve.seconds % 3600 / 60)
    seconds = math.floor(time_to_solve.seconds % 60)
    return f"{days} days and {hours}:{minutes}:{seconds}"