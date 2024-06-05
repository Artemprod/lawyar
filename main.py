import asyncio

from aiogram import Bot, Dispatcher

from openai import AsyncOpenAI

from bot.handlers import command_handler, user_handler, scenario_handlers
from bot.keyboards.main_menu import set_main_menu
from bot_configs import load_bot_config


async def main() -> None:
    config = load_bot_config(".env")
    client = AsyncOpenAI(api_key=config.chatGPT.key)

    # redis = Redis(host=config.redis_storage.host,
    #               port=config.redis_storage.port)
    # storage: RedisStorage = RedisStorage(redis=redis)

    bot: Bot = Bot(token=config.bot.tg_bot_token,
                   )

    dp: Dispatcher = Dispatcher(openai_client=client)
    dp.include_router(command_handler.router)
    dp.include_router(scenario_handlers.router)
    # dp.include_router(user_handler.router)
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == '__main__':
    # Запускаем бота
    asyncio.run(main())
