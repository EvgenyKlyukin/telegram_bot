from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


share_contact_button = KeyboardButton(
    text='📱 Поделиться контактом',
    request_contact=True
    )

accept_button = InlineKeyboardButton(
    text='Подтверждаю',
    callback_data='Подтверждаю'
    )

cancel_button = InlineKeyboardButton(
    text='Отменить запись',
    callback_data='Отменить запись'
    )

share_contact_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [share_contact_button]
    ]
)

survey_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [accept_button],
        [cancel_button]
        ]
        )
