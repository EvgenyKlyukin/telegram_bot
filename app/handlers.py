from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ContentType
from aiogram.filters import Command

from app.database import add_user, user_exists

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    keyboard = [
            [KeyboardButton(text="📱 Поделиться контактом",
                            request_contact=True)]
        ]
    await message.answer(('Здавствуйте! Нажмите кнопку "Поделиться контактом" '
                          'внизу, чтобы продолжить.'),
                          reply_markup=ReplyKeyboardMarkup(keyboard=keyboard))


@router.message(F.content_type == ContentType.CONTACT)
async def handle_contact(message):
    phone_number = message.contact.phone_number
    has_contact = user_exists(message.from_user.id)
    if not has_contact:
        add_user(message.from_user.id, phone_number)
        await message.answer("Данные успешно записаны!")
    else:
        await message.answer('Ваш номер уже есть в базе данных!')


@router.message()
async def message_handler(message: Message):
    has_contact = user_exists(message.from_user.id)
    if not has_contact:
        await message.answer('Нажмите кнопку "Поделиться контактом" '
                             'внизу, чтобы продолжить')
    else:
        await message.answer('Ваш номер уже есть в базе данных! '
                             'Мы сообщим Вам о записи на прием.')
