from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import CallbackQuery, Message

from tgbot.services.support import Support

class SupportMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, support_channel_id, bot_signature):
        super().__init__()
        self.support_channel_id = support_channel_id
        self.bot_signature = bot_signature

    async def pre_process(self, obj, data, *args):
        if isinstance(obj, Message):
            text = obj.text or obj.caption or ''
            if not text and obj.poll:
                text = obj.poll.question
        elif isinstance(obj, CallbackQuery):
            text = obj.data

        data["support"] = Support(self.manager.bot, self.support_channel_id, self.bot_signature)

    async def post_process(self, obj, data, *args):
        del data["support"]
