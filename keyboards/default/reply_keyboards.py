from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


add_sketch = KeyboardButton('📌Загрузить свой эскиз📌')
check_queue = KeyboardButton('🔍Проверить статус заказа🔍')

start = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
start.add(add_sketch, check_queue)