from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import upload_callback

post_check = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="OK",
            callback_data=upload_callback
        )
    ],
    [
        InlineKeyboardButton(
            text="Отмена",
            callback_data="cancel"
       )
    ]
])
