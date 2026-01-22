from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="OK",
                callback_data="OK",
            )]
        ]
    )
