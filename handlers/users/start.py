from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType
from loader import dp, bot
from data.config import ADMIN_ID
from utils.states import Order
import keyboards.default.reply_keyboards as kb
from utils.database import DBCommands
from aiogram.dispatcher import FSMContext

db = DBCommands()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await db.add_new_user()
    await message.answer(f'Привет, {message.from_user.full_name}! Здесь ты можешь заказать любой значок по фото',
                         reply_markup=kb.start)


@dp.message_handler(text='📌Загрузить свой эскиз📌', state='*')
async def sketch_handler(message: types.Message):
    await message.answer('Пришлите фото эскиза')
    await Order.photo.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=Order.photo)
async def photo_handler(message: types.Message, state: FSMContext):
    print(message.content_type)
    if message.photo:
        await state.update_data(message_id=message.message_id)
        await message.answer('Введите количество значков')
        await Order.quantity.set()
    else:
        await message.answer('Пришлите значок в формате картинки')


@dp.message_handler(state=Order.quantity)
async def quantity_handler(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        await bot.forward_message(ADMIN_ID, message.chat.id, data.get('message_id'))
        await bot.send_message(ADMIN_ID, f'Количество {message.text}')
        await db.add_new_order(int(message.text))
        await message.answer('Заказ принят. Если хотите добавить еще значок нажмите кнопку\n'
                             '<i>📌Загрузить свой эскиз📌</i>' )
        await state.reset_state()
    except:
        await message.answer('Произошла ошибка. Попробуйте еще раз')


@dp.message_handler(text="🔍Проверить статус заказа🔍", state='*')
async def queue_handler(message: types.Message):
    try:
        quantity = await db.get_quantity_order()
        await message.answer(f'Для формирования заказа осталось: {60 - int(quantity)} значков')
    except:
        await message.answer('Произошла ошибка попробуйте позже')



