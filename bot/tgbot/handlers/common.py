from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.models.role import UserRole
from tgbot.services.backend import Backend

# Dictionary handlers
async def translate(m: Message):
    await m.answer("<b>TRANSLATE WIDGET</b>")

# Fallbacks
async def rasa_fallback(m: Message, backend: Backend, nlu_data):
    try:
        response = nlu_data['response']
    except TypeError:
        await m.answer('Command is not supported yet')
        return
    await backend.save_chatlog(m.from_user.id, 'response', response)
    await m.answer(response)

def register_common(dp: Dispatcher):
    """Handlers available for any User"""
    # Dictionary handlers
    dp.register_message_handler(translate, intent="translate", state="*", chat_type='private', role=[UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT])
    # Fallbacks
    dp.register_message_handler(rasa_fallback, state="*", chat_type='private', role=[UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT])