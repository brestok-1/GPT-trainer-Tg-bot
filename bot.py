import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import load_config
from config_data.db_config import get_async_engine, get_async_sessionmaker, POSTGRES_URL
from handlers import user_handlers, other_handlers
from middlewares.register_check import RegisterCheck


async def main():
    logging.basicConfig(level=logging.INFO, format='%(filename)s:%(lineno)d #%(levelname)-8s '
                                                   '[%(asctime)s] - %(name)s - %(message)s')
    logging.info('Starting Bot')
    config = load_config()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    dp = Dispatcher()

    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    async_engine = get_async_engine(POSTGRES_URL)
    session_maker = get_async_sessionmaker(async_engine)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot has been stoped')
