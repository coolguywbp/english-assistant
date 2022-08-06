from aiogram import Dispatcher, Bot
from aiogram.types import Message, PreCheckoutQuery, ShippingQuery
from aiogram.types.message import ContentTypes

from tgbot.services.payment import Payment
from tgbot.services.rasa import Rasa
from tgbot.services.support import Support

from tgbot.models.role import UserRole

async def teacher_start(m: Message):
    # await repo.add_user(m.from_user.id)
    await m.reply("Hello, teacher!")

async def show_help(m: Message):
    await m.answer("<b>HELP MESSAGE</b>")

async def day_off(m: Message):
    await m.answer("<b>DAY OFF WIDGET</b>")
    
def register_teacher(dp: Dispatcher):
    dp.register_message_handler(teacher_start, commands=["start"], state="*", chat_type='private', role=UserRole.TEACHER)
    dp.register_message_handler(show_help, intent="help", state="*", chat_type='private', role=UserRole.TEACHER)
    
    dp.register_message_handler(day_off, intent="day_off", state="*", chat_type='private', role=UserRole.TEACHER)
    dp.register_message_handler(day_off, intent="day_off_today", state="*", chat_type='private', role=UserRole.TEACHER)
    dp.register_message_handler(day_off, intent="day_off_tomorrow", state="*", chat_type='private', role=UserRole.TEACHER)