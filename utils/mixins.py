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
