import asyncio
from aiogram import Bot, Dispatcher
from bot.settings import BOT_TOKEN
from bot.handlers import router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
