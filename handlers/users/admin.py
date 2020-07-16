from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import CallbackQuery

from data.config import ADMIN_ID
from loader import dp, bot
from utils.misc import rate_limit
from utils.database import DBCommands
from aiogram.dispatcher import FSMContext
from utils.states import Mailing
import keyboards.inline.inline_keyboards as kb

db = DBCommands()


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp(), filters.IDFilter(user_id=ADMIN_ID))
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку',
        '/status - Проверить количество заказов'
        '/clear - Обнулить список заказавших',
        '/mailing - сделать рассылку по пользователям'
    ]
    await message.answer('\n'.join(text))


@dp.message_handler(filters.IDFilter(user_id=ADMIN_ID), commands=['clear'])
async def clear_handler(message: types.Message):
    try:
        await db.clean_order_list()
        await message.answer('База очищена')
    except Exception as e:
        await message.answer(f'Произошла ошибка: {e}')


@dp.message_handler(filters.IDFilter(user_id=ADMIN_ID),commands=['mailing'])
async def mailing_handler(message: types.Message):
    await message.answer('Пришлите текст рассылки')
    await Mailing.text.set()


@dp.message_handler(state=Mailing.text)
async def mailing_handler(message: types.Message, state: FSMContext):
    await message.answer(f'Отправить рассылку? {message.text}',reply_markup=kb.confirm)
    await state.update_data(text=message.text)
    await Mailing.confirm.set()


@dp.callback_query_handler(lambda call: call.data in ['yes', 'no'], state=Mailing.confirm)
async def confirm_mailing(call: CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        data = await state.get_data()
        text = data.get('text')
        try:
            users = await db.get_all_users()
            for user in users:
                await bot.send_message(user.user_id, text=text)
            await call.message.answer('Рассылка успешно выполнена')
        except Exception as e:
            await call.message.answer(f'Во время рассылки произола ошибка: {e}')
    if call.data == 'no':
        await call.message.answer('Пришли другой текст рассылки')
        await Mailing.text.set()


@dp.message_handler(filters.IDFilter(user_id=ADMIN_ID), commands=['status'])
async def mailing_handler(message: types.Message):
    try:
        quantity = await db.get_quantity_order()
        await message.answer(f'Количество заказов: {quantity}')
    except Exception as e:
        await message.answer('Произошла ошибка попробуйте позже')