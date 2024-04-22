from aiogram.fsm.state import StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.dispatcher.dispatcher import MemoryStorage
import docs
import asyncio
import sqlite3
from functions import *
from aiogram import *
from aiogram.filters.command import Command
from aiogram.types import ContentType, InputMediaPhoto
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton, \
    InlineKeyboardMarkup
from base_connection import *
import re
import random
from kb import *

# архитектура бота
token = docs.token
bot = Bot(token)
dp = Dispatcher()
storage = MemoryStorage
# подключение бд
connection()


class OrderState(StatesGroup):
    waiting_for_description = State()
    waiting_for_budget = State()


class Support(StatesGroup):
    waiting_for_support = State()


# сообщения
answer = """
Привет! На нашей платформе ты сможешь получить квалифицированную помощь от лучших в своем деле
У нас ты сможешь найти помощь с домашними, контрольными, да вообще с любыми работами, которые тебе так не хочется делать
Давай познакомимся с тобой и решим кем ты зочешь стать на нашей платформе: решалой, который будет разносить задачи направо и налево, или же ты хочешь стать более свободным от навалившихся заданий человеком
"""
ans_stat_reshala = """
Отлично, у тебя есть возможностб помогать другим студентам через наш сервис и получать за это вознаграждение
Подтверди, действительно ли ты хочешь стать решалой?
Обращаем твое внимание на то, что,увы, нельзя одновременно быть и студентом и решалой
"""

ans_stat_dolboeb = """
Отлично, ты можешь запросить помощь у решал но тогда тебе придется прекратить свою деятельность решалы
"""


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(text=answer, reply_markup=keyboard1.as_markup())


@dp.message(Support.waiting_for_support)
async def ans(message: types.Message):
    text = message.text
    print(text)
    await bot.send_message(chat_id=message.chat.id, text='Ваше обращение зарегестрировано',
                           reply_markup=keyboard1.as_markup())


@dp.message(OrderState.waiting_for_description)
async def order_description(message: types.Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1].file_id  # Берем ID последней (наибольшей) фотографии
        await state.update_data(photo=photo)
    if message.text:
        await state.update_data(description=message.text)
    await state.set_state(OrderState.waiting_for_budget)
    await message.answer('Введите бюджет заказа в рублях')


@dp.message(OrderState.waiting_for_budget)
async def order_budget(message: types.Message, state: FSMContext):
    budget = re.findall(r'\d+', message.text)[0] if re.findall(r'\d+', message.text) else None
    if not budget:
        await message.answer("Пожалуйста, укажите бюджет цифрами.")
        return
    await state.update_data(budget=int(budget))

    user_data = await state.get_data()
    description = user_data.get('description', '')
    photo_id = user_data.get('photo', None)
    add_order(message.from_user.id, description, budget, photo_id)
    update_zakaz_status_student(message.from_user.id, True)
    # Здесь код для сохранения заказа в базу данных, включая описание, фото, бюджет и id студента

    await state.clear()
    await message.answer("Ваш заказ создан", reply_markup=keyboard9.as_markup())


@dp.message()
async def cmd_start(message: types.Message):
    if message.from_user.id == 985024736 and message.text.lower() == 'инфо':
        await message.answer(sobrat_info_users())
        await message.answer(sobrat_info_teachers())
        await message.answer(sobrat_info_orders())


@dp.callback_query(F.data == 'confirm')
async def confirm_cmd(callback_query: types.CallbackQuery):
    delete_user(callback_query.from_user.id)
    dobavit_teacher(callback_query.from_user.id)
    update_cnt_teacher(callback_query.from_user.id, 0)

    update_zakaz_status_teacher(callback_query.from_user.id, False)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text='Отличное, вот твое меню', reply_markup=keyboard2.as_markup())


@dp.callback_query(F.data == 'cancel')
async def cancel_cmd(callback_query: types.CallbackQuery):
    if proof_reshala(callback_query.from_user.id):
        if not status_teacher(callback_query.from_user.id):
            await callback_query.message.edit_text('Меню',
                                                   reply_markup=keyboard2.as_markup(resize_keyboard=True,
                                                                                    one_time_keyboard=True))
        else:
            await callback_query.message.edit_text('Меню',
                                                   reply_markup=keyboard11.as_markup(resize_keyboard=True,
                                                                                     one_time_keyboard=True))
    elif proof_student(callback_query.from_user.id):
        if status_student(callback_query.from_user.id):
            await callback_query.message.edit_text(text='Меню', reply_markup=keyboard9.as_markup())
        else:
            await callback_query.message.edit_text('Меню',
                                                   reply_markup=keyboard1.as_markup(resize_keyboard=True,
                                                                                    one_time_keyboard=True))


@dp.callback_query(F.data == 'menu')
async def cancel_cmd(callback_query: types.CallbackQuery):
    update_cnt_teacher(callback_query.from_user.id, 0)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Меню', reply_markup=keyboard2.as_markup())


@dp.callback_query(F.data == 'new_order')
async def new_order(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.waiting_for_description)
    await callback_query.message.edit_text(text='Отправьте описание заказа (текст и/или фото)',
                                           reply_markup=keyboard10.as_markup())


@dp.callback_query(F.data == 'my_orders')
async def new_order(callback_query: types.CallbackQuery):
    pass


@dp.callback_query(F.data == 'complete_orders')
async def new_order(callback_query: types.CallbackQuery):
    pass


@dp.callback_query(F.data == 'support')
async def new_order(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Support.waiting_for_support)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Отправьте сообщение для поддержки',
                           reply_markup=keyboard15.as_markup())


@dp.callback_query(F.data == 'new_life')
async def new_order(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(ans_stat_reshala,
                                           reply_markup=keyboard3.as_markup(resize_keyboard=True,
                                                                            one_time_keyboard=True))


@dp.callback_query(F.data == 'support')
async def new_order(callback_query: types.CallbackQuery):
    pass


@dp.callback_query(F.data == 'new_orders')
async def new_order(callback_query: types.CallbackQuery):
    mas = get_order_by_index(dostat_cnt_teacher(callback_query.from_user.id))
    ans = 'Описание заказа:' + '\n' + str(mas[2]) + '\n' + 'Бюджет: ' + str(mas[6] * 0.85)
    if mas[7]:
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await bot.send_photo(chat_id=callback_query.message.chat.id, photo=mas[7], caption=ans,
                             reply_markup=keyboard7.as_markup())
    else:
        await callback_query.message.edit_text(text=ans, reply_markup=keyboard7.as_markup())


@dp.callback_query(F.data == 'profile')
async def new_order(callback_query: types.CallbackQuery):
    pass


@dp.callback_query(F.data == 'da')
async def new_order(callback_query: types.CallbackQuery):
    dobavit_otklik(callback_query.from_user.id, dostat_cnt_teacher(callback_query.from_user.id))
    await callback_query.message.edit_text('Ваш отклик зарегестирован',
                                           reply_markup=keyboard2.as_markup(resize_keyboard=True,
                                                                            one_time_keyboard=True))


@dp.callback_query(F.data == 'net')
async def new_order(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Меню',
                           reply_markup=keyboard2.as_markup(resize_keyboard=True,
                                                            one_time_keyboard=True))


@dp.callback_query(F.data == 'nachalo')
async def new_order(callback_query: types.CallbackQuery):
    update_cnt_teacher(callback_query.from_user.id, 0)
    mas = get_order_by_index(dostat_cnt_teacher(callback_query.from_user.id))
    ans = 'Описание заказа:' + '\n' + str(mas[2]) + '\n' + 'Бюджет: ' + str(mas[6] * 0.85)
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    if mas[7]:
        await bot.send_photo(chat_id=callback_query.message.chat.id, photo=mas[7], caption=ans,
                             reply_markup=keyboard7.as_markup())
    else:
        await bot.send_message(chat_id=callback_query.message.chat.id, text=ans,
                               reply_markup=keyboard7.as_markup())


@dp.callback_query(F.data == 'previous')
async def new_order(callback_query: types.CallbackQuery):
    a = dostat_cnt_teacher(callback_query.from_user.id)
    update_cnt_teacher(callback_query.from_user.id, a - 1)
    mas = get_order_by_index(dostat_cnt_teacher(callback_query.from_user.id))
    ans = 'Описание заказа:' + '\n' + str(mas[2]) + '\n' + 'Бюджет: ' + str(int(mas[6] * 0.85))
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    if a == 1:
        if mas[7]:
            await bot.send_photo(chat_id=callback_query.message.chat.id, photo=mas[7], caption=ans,
                                 reply_markup=keyboard7.as_markup())
        else:
            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text=ans,
                                   reply_markup=keyboard7.as_markup())
    else:
        if mas[7]:
            await bot.send_photo(chat_id=callback_query.message.chat.id, photo=mas[7], caption=ans,
                                 reply_markup=keyboard6.as_markup())
        else:
            await bot.send_message(chat_id=callback_query.message.chat.id, text=ans, reply_markup=keyboard6.as_markup())


@dp.callback_query(F.data == 'otmena')
async def otmena(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Меню', reply_markup=keyboard1.as_markup())


@dp.callback_query(F.data == 'done')
async def new_order(callback_query: types.CallbackQuery):
    dobavit_otklik(id_teacher=callback_query.message.chat.id, id_zakaz=dostat_cnt_teacher(callback_query.from_user.id))
    await bot.send_message(chat_id=callback_query.message.chat.id, text='твой отклик зарегестрирован',
                           reply_markup=keyboard2.as_markup())


@dp.callback_query(F.data == 'next')
async def new_order(callback_query: types.CallbackQuery):
    a = dostat_cnt_teacher(callback_query.from_user.id)
    update_cnt_teacher(callback_query.from_user.id, a + 1)
    mas = get_order_by_index(dostat_cnt_teacher(callback_query.from_user.id))

    if mas != False:
        ans = 'Описание заказа:' + '\n' + str(mas[2]) + '\n' + 'Бюджет: ' + str(int(int(mas[6]) * 0.85))
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        if a == cnt_orders() - 2:
            if mas[7]:
                await bot.send_photo(chat_id=callback_query.message.chat.id, photo=mas[7], caption=ans,
                                     reply_markup=keyboard8.as_markup())
            else:
                await bot.send_message(chat_id=callback_query.message.chat.id, text=ans,
                                       reply_markup=keyboard8.as_markup())
        else:
            if mas[7]:
                await bot.send_photo(chat_id=callback_query.message.chat.id, photo=mas[7], caption=ans,
                                     reply_markup=keyboard6.as_markup())
            else:
                await bot.send_message(chat_id=callback_query.message.chat.id, text=ans,
                                       reply_markup=keyboard6.as_markup())


@dp.callback_query(F.data == 'konec')
async def new_order(callback_query: types.CallbackQuery):
    update_cnt_teacher(callback_query.from_user.id, cnt_orders() - 1)
    mas = get_order_by_index(dostat_cnt_teacher(callback_query.from_user.id))
    ans = 'Описание заказа:' + '\n' + str(mas[2]) + '\n' + 'Бюджет: ' + str(int(int(mas[6]) * 0.85))
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    if mas[7]:
        await bot.send_photo(chat_id=callback_query.message.chat.id, photo=mas[7], caption=ans,
                             reply_markup=keyboard6.as_markup())
    else:
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text=ans,
                               reply_markup=keyboard8.as_markup())


@dp.callback_query(F.data == 'nazad')
async def new_order(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    if proof_reshala(callback_query.from_user.id):
        if status_teacher(callback_query.from_user.id):
            await bot.send_message(chat_id=callback_query.message.chat.id, text='Меню',
                                   reply_markup=keyboard11.as_markup())
        else:
            await bot.send_message(chat_id=callback_query.message.chat.id, text='Меню',
                                   reply_markup=keyboard2.as_markup())
    else:
        if status_student(callback_query.from_user.id):
            await bot.send_message(chat_id=callback_query.message.chat.id, text='Меню',
                                   reply_markup=keyboard9.as_markup())
        else:
            await state.clear()
            await bot.send_message(chat_id=callback_query.message.chat.id, text='Меню',
                                   reply_markup=keyboard1.as_markup())


@dp.callback_query(F.data == 'choose_teacher')
async def new_order(callback_query: types.CallbackQuery, state: FSMContext):
    update_cnt_student(callback_query.from_user.id, 0)
    mas = get_otkliki(dostat_id_zakaza(callback_query.from_user.id), dostat_cnt_student(callback_query.from_user.id))
    ans = ''
    for elem in mas:
        ans += str(elem) + '\n'
    await callback_query.message.edit_text(text=ans, reply_markup=keyboard13.as_markup())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
