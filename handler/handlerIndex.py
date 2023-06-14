from infra.servererror import ErrorServer
from .handler import Handler
from settings import ENVIRONMENT,SERVER_NAME,SERVER_VERSION


class HandlerIndex(Handler):

    def get(self):
        try:
            return self.toJson({
                "Server": SERVER_NAME,
                "Version": SERVER_VERSION,
                "environment": ENVIRONMENT,
            })
        except ErrorServer as e:
            e.get()
            return e.error