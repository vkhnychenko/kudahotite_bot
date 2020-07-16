from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm = InlineKeyboardMarkup(row_width=1)
confirm.insert(InlineKeyboardButton('Да', callback_data='yes'))
confirm.insert(InlineKeyboardButton('Нет', callback_data='no'))

