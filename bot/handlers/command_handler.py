from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.inline_keyboards import crete_inline_keyboard_assistants

# from bot.keyboards.inline_keyboards import crete_inline_keyboard_options

router = Router()


@router.message(CommandStart(), )
async def process_start_command(message: Message):
    option_keyboard = crete_inline_keyboard_assistants()
    await message.answer(text='Выбери сценарий', reply_markup=option_keyboard)
