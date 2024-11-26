from aiogram import Router, F

from aiogram.types import Message, ContentType, ReplyKeyboardRemove, \
    CallbackQuery

from aiogram.filters import Command

from app.database import add_user, user_exists

from app.keyboards import share_contact_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        ('Здавствуйте! Нажмите кнопку "Поделиться контактом" '
         'внизу, чтобы продолжить.'),
         reply_markup=share_contact_keyboard
         )


@router.message(F.content_type == ContentType.CONTACT)
async def handle_contact(message):
    phone_number = message.contact.phone_number
    has_contact = user_exists(message.from_user.id)
    if not has_contact:
        add_user(message.from_user.id, phone_number)
        await message.answer("Данные успешно записаны!",
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Ваш номер уже есть в базе данных!',
                             reply_markup=ReplyKeyboardRemove())


@router.message()
async def message_handler(message: Message):
    has_contact = user_exists(message.from_user.id)
    if not has_contact:
        await message.answer('Нажмите кнопку "Поделиться контактом" '
                             'внизу, чтобы продолжить')
    else:
        await message.answer('Ваш номер уже есть в базе данных! '
                             'Мы сообщим Вам о записи на прием.')


# @router.callback_query(F.data == 'Подтверждаю')
# async def process_callback_accept(call: CallbackQuery):
#     await call.message.answer('Запись подтверждена',
#                               show_alert=True)


# @router.callback_query(F.data == 'Отменить запись')
# async def process_callback_cancel(call: CallbackQuery):
#     await call.message.answer('Запись отменена',
#                               show_alert=True)


# @router.callback_query(F.data == 'Подтверждаю')
# async def process_callback_accept(call: CallbackQuery):
#     await bot.delete_message(chat_id=call.from_user.id,
#                              message_id=call.message.message_id)
#     await call.message.answer('Запись подтверждена')
