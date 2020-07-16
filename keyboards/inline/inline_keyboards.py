from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm = InlineKeyboardMarkup(row_width=1)
confirm.insert(InlineKeyboardButton('Всем пользователям', callback_data='all'))
confirm.insert(InlineKeyboardButton('Кто делал заказ', callback_data='order'))

