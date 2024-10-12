import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers import router

TOKEN = '7479878968:AAGGk5BaXBPlnWN_upsc5s56Y6peme62r1g'

LOG_FORMAT = ("[%(asctime)s.%(msecs)03d]"
              "%(module)s:%(lineno)d %(levelname)-7s - %(message)s")


async def main():
    """
    Основная функция бота, которая выполняет создание объектов,
    мониторинг апдейтов и передачу апдейтов в обработчики.
    """
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Подключает к диспетчеру все обработчики, которые используют router.
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        filename=r'log\logging.log',
                        format=LOG_FORMAT)
    asyncio.run(main())