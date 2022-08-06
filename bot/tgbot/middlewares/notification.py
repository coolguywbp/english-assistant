from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

class NotificationMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, notification):
        super().__init__()
        self.notification = notification

    async def pre_process(self, obj, data, *args):
        data["notification"] = self.notification

    async def post_process(self, obj, data, *args):
        del data["notification"]
