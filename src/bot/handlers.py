from aiogram import Router, types
from bot.keyboard import main_keyboard

router = Router()


@router.message(lambda m: m.text == "A")
async def press_a(message: types.Message):
    await message.answer("You pressed A")


@router.message(lambda m: m.text == "B")
async def press_b(message: types.Message):
    await message.answer("You pressed B")


@router.message()
async def default(message: types.Message):
    await message.answer(
        "Choose:",
        reply_markup=main_keyboard(),
    )
