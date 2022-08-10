from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.models.role import UserRole
from tgbot.services.support import Support

async def admin_start(m: Message):
    await m.reply("Hello, admin!")

async def show_help(m: Message):
    await m.answer("<b>ADMIN HELP MESSAGE</b>")
    
async def answer_issue(m: Message, support: Support):
    # await support.answer_issue(m)
    pass

def register_admin(dp: Dispatcher):
    """Handlers for Admins"""
    dp.register_message_handler(admin_start, commands=["start"], state="*", role=UserRole.ADMIN)
    dp.register_message_handler(show_help, commands=["help"], state="*", chat_type='private', role=UserRole.ADMIN)
    dp.register_message_handler(show_help, intent="help", state="*", chat_type='private', role=UserRole.ADMIN)
    
    dp.register_message_handler(answer_issue, state="*",  is_reply=True, chat_type='supergroup', role=UserRole.ADMIN)
