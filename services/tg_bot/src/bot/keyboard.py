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


def left_right_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Left",
                    callback_data="LEFT",
                ),
                InlineKeyboardButton(
                    text="Right",
                    callback_data="RIGHT",
                ),
            ]
        ]
    )
