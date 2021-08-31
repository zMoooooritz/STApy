from enum import Enum

class Request(Enum):
    """
    This class represents all available requests in the SensorThingsAPI (v1.1)
    """
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"

    @staticmethod
    def list():
        """
        :return: a list of all request values
        """
        return list(map(lambda r: r.value, Request))
