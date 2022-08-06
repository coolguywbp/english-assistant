from aiogram import Dispatcher, Bot
from aiogram.types import Message, PreCheckoutQuery, ShippingQuery
from aiogram.types.message import ContentTypes

from tgbot.services.payment import Payment
from tgbot.services.rasa import Rasa

from tgbot.models.role import UserRole

# Dictionary handlers
async def translate(m: Message):
    await m.answer("<b>TRANSLATE WIDGET</b>")

# Fallbacks
async def rasa_fallback(m: Message, nlu_data):
    response = nlu_data['response']
    await m.answer(response)

def register_common(dp: Dispatcher):
    # Dictionary handlers
    dp.register_message_handler(translate, intent="translate", state="*", chat_type='private', role=[UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT])
    # Fallbacks
    dp.register_message_handler(rasa_fallback, state="*", chat_type='private', role=[UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT])