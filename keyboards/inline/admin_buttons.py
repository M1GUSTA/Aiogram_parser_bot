from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import db_callback

admin_choice = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Изменить парсер",
                                                callback_data=db_callback.new(db_name="VK_posts")
                                            ),
                                            InlineKeyboardButton(
                                                text="Купить яблоки",
                                                callback_data=db_callback.new(db_name="users")
                                            )
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text="Отмена",
                                                callback_data="cancel"
                                            )
                                        ]
                                    ])
source_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Отмена",
            callback_data="cancel"
        )
    ]
])
another_try = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Попробовать еще раз",
            callback_data="retry"
        )
    ],
    [
        InlineKeyboardButton(
            text="Отмена",
            callback_data="cancel"
       )
    ]
])
