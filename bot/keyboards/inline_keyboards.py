from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.lexicon.keyboards import cases


def crete_inline_keyboard_assistants():

    kp_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for key, value in cases.items():
        kp_builder.button(
            text=f"{value}",
            callback_data=f"{key}"
        )


    kp_builder.adjust(2)
    return kp_builder.as_markup()

def crete_inline_keyboard_ready():

    kp_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kp_builder.button(
        text=f"Загрузил",
        callback_data=f"ready")



    kp_builder.adjust(2)
    return kp_builder.as_markup()