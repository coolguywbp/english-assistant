import logging
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import CallbackQuery, Message

class RasaMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, rasa):
        super().__init__()
        self.rasa = rasa
        self.logger = logging.getLogger('RASA_MIDDLEWARE')

    async def pre_process(self, obj, data, *args):
        if isinstance(obj, Message):
            text = obj.text or obj.caption or ''
            user_id = obj.from_user.id
            if not text and obj.poll:
                text = obj.poll.question
        elif isinstance(obj, CallbackQuery):
            text = obj.data
            user_id = obj.chat.id
            
        data["nlu_data"] = None
        data["intent"] = None
        
        """Getting Rasa data with every text message (only in private chat and not commands)"""
        if (obj.chat.type == 'private' and obj.entities[0].type != 'bot_command'):
            nlu_data = await self.rasa.get_data(user_id, data['role'], text)
            intent = nlu_data['intent']
            data["nlu_data"] = nlu_data
            data["intent"] = intent['name']

    async def post_process(self, obj, data, *args):
        try:
            del data["nlu_data"]
            del data["intent"]
        except KeyError:
            pass
