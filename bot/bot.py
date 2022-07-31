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
from tgbot.handlers.user import register_user

from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.middlewares.payment import PaymentMiddleware
from tgbot.middlewares.rasa import RasaMiddleware
from tgbot.middlewares.support import SupportMiddleware

from tgbot.services.rasa import Rasa

logger = logging.getLogger(__name__)

def create_pool(user, password, database, host, echo):
    raise NotImplementedError  # TODO check your db connector

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

    # dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(os.environ["admin_id"]))
    dp.middleware.setup(PaymentMiddleware(os.environ["payment_token"]))
    dp.middleware.setup(RasaMiddleware(rasa))
    dp.middleware.setup(SupportMiddleware(os.environ["support_channel_id"], os.environ["signature"]))

    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IntentFilter)

    register_admin(dp)
    register_user(dp)

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
