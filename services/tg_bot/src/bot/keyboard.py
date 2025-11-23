from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="A"), KeyboardButton(text="B")]
        ],
        resize_keyboard=True
    )
