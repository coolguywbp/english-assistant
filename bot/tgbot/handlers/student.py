from aiogram import Dispatcher, Bot
from aiogram.types import Message, PreCheckoutQuery, ShippingQuery
from aiogram.types.message import ContentTypes

from tgbot.models.role import UserRole

from tgbot.services.payment import Payment
from tgbot.services.rasa import Rasa
from tgbot.services.support import Support

async def student_start(m: Message):
    await m.reply("Hello, student!")

async def student_help(m: Message):
    await m.answer("<b>HELP MESSAGE</b>")
    
# Calls handlers
async def new_call(m: Message):
    await m.answer("<b>NEW CALL WIDGET</b>")

async def show_calls(m: Message):
    await m.answer("<b>SHOW CALLS WIDGET</b>")
    
# Account handlers
async def change_teacher(m: Message):
    await m.answer("<b>CHANGE TEACHER WIDGET</b>")

async def show_plans(m: Message):
    await m.answer("<b>CHOOSE PLAN WIDGET</b>")

# Practice handlers
async def wordpractice(m: Message):
    await m.answer("<b>WORDPRACTICE WIDGET</b>")

# Support handlers
async def start_issue(m: Message, support: Support, nlu_data):
    await support.start_issue(m, nlu_data['text'])
    await m.answer("<b>SUPPORT</b>")
    
# Dictionary handlers
async def translate(m: Message):
    await m.answer("<b>TRANSLATE WIDGET</b>")
    
# Payment handlers
async def start_purchase(m: Message, payment: Payment):
    await m.reply("Starting payment!")
    await payment.send_invoice()

async def shipping(shipping_query: ShippingQuery, payment: Payment):
    print('Shipping query:\n', shipping_query)
    await payment.answer_shipping_query(shipping_query.id)

async def checkout(pre_checkout_query: PreCheckoutQuery, payment: Payment):
    print('Pre checkout query:\n', pre_checkout_query)
    await payment.answer_pre_checkout_query(pre_checkout_query.id)

async def got_payment(m: Message):
    await m.reply("Yohoo!")
    await m.reply("У нас твои {amount}{currency}!".format(amount=m.successful_payment.total_amount / 100, currency=m.successful_payment.currency))

def register_student(dp: Dispatcher):
    """Handlers for Students"""
    dp.register_message_handler(student_start, commands=["start"], state="*", chat_type='private', role=UserRole.STUDENT)
    dp.register_message_handler(student_help, commands=["help"], state="*", chat_type='private', role=UserRole.STUDENT)
    dp.register_message_handler(student_help, intent="help", state="*", chat_type='private', role=UserRole.STUDENT)
    # Calls handlers
    dp.register_message_handler(new_call, intent="new_call", state="*", chat_type='private', role=UserRole.STUDENT)
    dp.register_message_handler(show_calls, intent="show_calls", state="*", chat_type='private', role=UserRole.STUDENT)
    # Account handlers
    dp.register_message_handler(change_teacher, intent="change_teacher", state="*", chat_type='private', role=UserRole.STUDENT)
    dp.register_message_handler(show_plans, intent="show_plans", state="*", chat_type='private', role=UserRole.STUDENT)
    # Practice handlers
    dp.register_message_handler(wordpractice, intent="wordpractice", state="*", chat_type='private', role=UserRole.STUDENT)
    # Support handlers
    dp.register_message_handler(start_issue, intent="support", state="*", chat_type='private', role=UserRole.STUDENT)
    # Payment handlers
    dp.register_message_handler(start_purchase, commands=["buy"], state="*", chat_type='private', role=UserRole.STUDENT)
    dp.register_shipping_query_handler(shipping, lambda query: True, role=UserRole.STUDENT)
    dp.register_pre_checkout_query_handler(checkout, lambda query: True, role=UserRole.STUDENT)
    dp.register_message_handler(got_payment, content_types=ContentTypes.SUCCESSFUL_PAYMENT, role=UserRole.STUDENT)
