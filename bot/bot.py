import sys
sys.path.append('../')

import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.filters.intent import IntentFilter

from tgbot.handlers.admin import register_admin
from tgbot.handlers.student import register_student
from tgbot.handlers.teacher import register_teacher
from tgbot.handlers.common import register_common
from tgbot.handlers.channel import register_channel

from tgbot.middlewares.backend import BackendMiddleware
from tgbot.middlewares.payment import PaymentMiddleware
from tgbot.middlewares.rasa import RasaMiddleware
from tgbot.middlewares.support import SupportMiddleware
from tgbot.middlewares.notification import NotificationMiddleware

from tgbot.services.rasa import Rasa
from tgbot.services.backend import Backend
from tgbot.services.notification import Notification

def get_updates_in_use(dp: Dispatcher):
    available_updates = (
        "callback_query_handlers", "channel_post_handlers", "chat_member_handlers",
        "chosen_inline_result_handlers", "edited_channel_post_handlers", "edited_message_handlers",
        "inline_query_handlers", "message_handlers", "my_chat_member_handlers", "poll_answer_handlers",
        "poll_handlers", "pre_checkout_query_handlers", "shipping_query_handlers", "chat_join_request_handlers"
    )
    return [item.replace("_handlers", "") for item in available_updates if len(dp.__getattribute__(item).handlers) > 0]

logger = logging.getLogger(__name__)

async def main():
    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    
    # Storage
    if os.environ["use_redis"].lower() == 'true':
        storage = RedisStorage()
    else:
        storage = MemoryStorage()

    bot = Bot(token=os.environ["token"], parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)
    
    # Services
    rasa = Rasa(bot, os.environ["log_channel_id"])
    backend = Backend(os.environ["backend_host"])
    notification = Notification(bot, os.environ["lobby_channel_id"])
    
    # Middlewares
    dp.middleware.setup(BackendMiddleware(backend))
    dp.middleware.setup(NotificationMiddleware(notification))
    dp.middleware.setup(PaymentMiddleware(os.environ["payment_token"]))
    dp.middleware.setup(SupportMiddleware(os.environ["support_channel_id"], os.environ["signature"]))
    dp.middleware.setup(RasaMiddleware(rasa))

    # Filters
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IntentFilter)

    # Handlers
    register_admin(dp)
    register_teacher(dp)
    register_student(dp)
    register_common(dp)
    register_channel(dp)
    
    # Start
    try:
        await dp.start_polling(allowed_updates=get_updates_in_use(dp))
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")