from aiogram import Bot
from aiogram.types import BotCommand

from bot.lexicon.keyboards import main_menu


async def set_main_menu(bot:Bot)->None:
    main_menu_commands = [BotCommand(command=command, description=description)
                          for command, description in main_menu.items()]
    await bot.set_my_commands(main_menu_commands)
