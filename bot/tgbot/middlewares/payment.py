from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from tgbot.services.payment import Payment

class PaymentMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, token):
        super().__init__()
        self.token = token

    async def pre_process(self, obj, data, *args):
        data["payment"] = Payment(self.token, self.manager.bot, obj.from_user.id)

    async def post_process(self, obj, data, *args):
        del data["payment"]
