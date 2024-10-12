from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command("start")) # Нужно редактировать
async def start_handler(message: Message):
    await message.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")


@router.message() # Нужно редактировать
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID:")