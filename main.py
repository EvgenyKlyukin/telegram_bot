import asyncio

import logging

from aiogram import Bot, Dispatcher, F

from app.handlers import router

from settings import token, send_message_hour, send_message_minute

from app.database import id_telegram_users, checklist, worker_speciality

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.keyboards import survey_keyboard

from aiogram.types import CallbackQuery

bot = Bot(token=token)
dp = Dispatcher()


async def main():
    """
    Основная функция бота, которая выполняет создание объектов,
    мониторинг апдейтов и передачу апдейтов в обработчики.
    """
    logging.info('Запуск бота.')
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(
        notifications_sandler,
        trigger='cron',
        hour=send_message_hour,
        minute=send_message_minute
        )
    scheduler.start()

    # Подключает к диспетчеру все обработчики, которые используют router.
    dp.include_router(router)
    await bot.delete_webhook()
    await dp.start_polling(bot)


async def notifications_sandler():
    result = checklist()
    logging.info('[notifications_sandler] - Начал работу.')
    logging.info(f'[notifications_sandler] - Найдено {len(result)} записей '
                 'для уведомлений.')
    for i in result:
        message = (
            'Доброго времени суток!\n'
            f'Вы записаны {i[0]} в {i[1]} к {worker_speciality(i[3])}\n'
            'Ждем Вас в нашей клинике.\n'
            'Наш адрес: ул. Ивана Захарова, 1\n'
            'Телефон для связи: +7 999 999-99-99'
        )
        try:
            logging.info('[notifications_sandler] - Отправка сообщения '
                         f'пользователю {id_telegram_users(i[2])}.')
            await bot.send_message(chat_id=str(id_telegram_users(i[2])),
                                   text=message,
                                   reply_markup=survey_keyboard)
        except Exception as e:
            logging.error('[notifications_sandler] - Ошибка при отправке '
                          f'сообщения: {e}')
    logging.info('[notifications_sandler] - Закончил работу.')


@dp.callback_query(F.data == 'Подтверждаю')
async def process_callback_accept(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)
    await call.message.answer('Запись подтверждена')


@dp.callback_query(F.data == 'Отменить запись')
async def process_callback_accept(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)
    await call.message.answer('Запись отменена')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        filename=r'log\logging.log',
                        format=("[%(asctime)s.%(msecs)03d]"
                                "%(module)s:%(lineno)d "
                                "%(levelname)-7s - %(message)s"),
                        encoding='utf-8')
    asyncio.run(main())
