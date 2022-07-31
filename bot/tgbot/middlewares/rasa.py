from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import CallbackQuery, Message

class RasaMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, rasa):
        super().__init__()
        self.rasa = rasa

    async def pre_process(self, obj, data, *args):
        if isinstance(obj, Message):
            text = obj.text or obj.caption or ''
            user_id = obj.from_user.id
            if not text and obj.poll:
                text = obj.poll.question
        elif isinstance(obj, CallbackQuery):
            text = obj.data
            user_id = obj.chat.id
        if (obj.chat.type == 'private'):
            nlu_data = await self.rasa.get_data(user_id, text)
            intent = nlu_data['intent']
            # data["rasa"] = self.rasa
            data["nlu_data"] = nlu_data
            data["intent"] = intent['name']

    async def post_process(self, obj, data, *args):
        try:
            del data["nlu_data"]
            del data["intent"]
        except KeyError:
            pass
