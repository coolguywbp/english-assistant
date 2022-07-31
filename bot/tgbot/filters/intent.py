import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types.base import TelegramObject


class IntentFilter(BoundFilter):
    key = 'intent'

    def __init__(self, intent = None):
        self.intent = intent

    async def check(self, obj: TelegramObject):
        data = ctx_data.get()
        data.get("intent")
        return data.get("intent") == self.intent
