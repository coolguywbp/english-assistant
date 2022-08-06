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

from tgbot.middlewares.backend import BackendMiddleware
from tgbot.middlewares.payment import PaymentMiddleware
from tgbot.middlewares.rasa import RasaMiddleware
from tgbot.middlewares.support import SupportMiddleware

from tgbot.services.rasa import Rasa
from tgbot.services.backend import Backend

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    
    if os.environ["use_redis"].lower() == 'true':
        storage = RedisStorage()
    else:
        storage = MemoryStorage()

    bot = Bot(token=os.environ["token"], parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)
    
    rasa = Rasa(bot, os.environ["log_channel_id"])
    backend = Backend(os.environ["backend_host"])

    dp.middleware.setup(BackendMiddleware(backend))
    dp.middleware.setup(RasaMiddleware(rasa))
    dp.middleware.setup(PaymentMiddleware(os.environ["payment_token"]))
    dp.middleware.setup(SupportMiddleware(os.environ["support_channel_id"], os.environ["signature"]))

    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IntentFilter)

    register_admin(dp)
    register_teacher(dp)
    register_student(dp)
    register_common(dp)

    # start bot
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
