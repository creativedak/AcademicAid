from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from functions import *
'''
def opredelit_kb(id):
    if proof_reshala(id):
        if status_teacher(id):
            return keyboard11
        else:
            return keyboard2
    elif proof_student(id):
        if status_student(id):
            return keyboard9
        else:
            return keyboard1
    else:
        dobavit_user(id)
        return keyboard1
'''
# меню долбоеба полное
keyboard1 = InlineKeyboardBuilder()
keyboard1.row(InlineKeyboardButton(text='Выложить задание', callback_data='new_order'),
              InlineKeyboardButton(text="Список моих заказов", callback_data='my_orders'))
keyboard1.row(InlineKeyboardButton(text="Список всех заказов", callback_data='complete_orders'),
              InlineKeyboardButton(text="Поддержка", callback_data='support'),
              InlineKeyboardButton(text="Стать решалой", callback_data='new_life'))

# меню долбоеба при заказе
keyboard9 = InlineKeyboardBuilder()
keyboard9.row(InlineKeyboardButton(text='Выбрать решалу', callback_data='choose_teacher'),
              InlineKeyboardButton(text='Оплатить заказ', callback_data='payment'))
keyboard9.row(InlineKeyboardButton(text='Завершить заказ', callback_data='sdelano'),
              InlineKeyboardButton(text='Поддержка', callback_data='support'))

# меню решалы
keyboard2 = InlineKeyboardBuilder()
keyboard2.row(InlineKeyboardButton(text='Доступные заказы', callback_data='new_orders'))
keyboard2.row(InlineKeyboardButton(text="Профиль", callback_data='profile'),
              InlineKeyboardButton(text="Поддержка", callback_data='support'))

# меню решалы при заказе
keyboard11 = InlineKeyboardBuilder()
keyboard11.row(InlineKeyboardButton(text='Отправить решение', callback_data='gotovo'))
keyboard11.row(InlineKeyboardButton(text='Связаться с заказчиком', callback_data='chat'),
               InlineKeyboardButton(text='Поддержка', callback_data='support'))

# стать решалой
keyboard3 = InlineKeyboardBuilder()
keyboard3.row(InlineKeyboardButton(text='ДА', callback_data='confirm'))
keyboard3.row(InlineKeyboardButton(text='нажал случайно', callback_data='cancel'))

# подтвердить работу
keyboard5 = InlineKeyboardBuilder()
keyboard5.row(InlineKeyboardButton(text='ДА', callback_data='da'))
keyboard5.row(InlineKeyboardButton(text='нажал случайно', callback_data='net'))

# доатсупные заказы со 2 по предпоследний
keyboard6 = InlineKeyboardBuilder()
keyboard6.row(InlineKeyboardButton(text='К началу', callback_data='nachalo'))
keyboard6.row(InlineKeyboardButton(text='Предыдущий заказ', callback_data='previous'))
keyboard6.row(InlineKeyboardButton(text='Взяться за работу', callback_data='done'))
keyboard6.row(InlineKeyboardButton(text='Следуюший заказ', callback_data='next'))
keyboard6.row(InlineKeyboardButton(text='В конец', callback_data='konec'))
keyboard6.row(InlineKeyboardButton(text='Меню', callback_data='menu'))

# первый заказ
keyboard7 = InlineKeyboardBuilder()
keyboard7.row(InlineKeyboardButton(text='Взяться за работу', callback_data='done'))
keyboard7.row(InlineKeyboardButton(text='Следуюший заказ', callback_data='next'))
keyboard7.row(InlineKeyboardButton(text='В конец', callback_data='konec'))
keyboard7.row(InlineKeyboardButton(text='Меню', callback_data='menu'))

# последний заказ
keyboard8 = InlineKeyboardBuilder()
keyboard8.row(InlineKeyboardButton(text='К началу', callback_data='nachalo'))
keyboard8.row(InlineKeyboardButton(text='Предыдущий заказ', callback_data='previous'))
keyboard8.row(InlineKeyboardButton(text='Взяться за работу', callback_data='done'))
keyboard8.row(InlineKeyboardButton(text='Меню', callback_data='menu'))

# отмена
keyboard10 = InlineKeyboardBuilder()
keyboard10.row(InlineKeyboardButton(text='Отмена', callback_data='nazad'))

# выбор решалы со 2 по n-1
keyboard12 = InlineKeyboardBuilder()
keyboard12.row(InlineKeyboardButton(text='◀️', callback_data='prev'),
               InlineKeyboardButton(text='Выбрать решалу', callback_data='gotovo'),
               InlineKeyboardButton(text='▶️', callback_data='sled'))
keyboard12.row(InlineKeyboardButton(text='меню', callback_data='menu'))

# выбор решалы первый
keyboard13 = InlineKeyboardBuilder()
keyboard13.row(
    InlineKeyboardButton(text='Выбрать решалу', callback_data='gotovo'),
    InlineKeyboardButton(text='▶️', callback_data='sled'))
keyboard13.row(InlineKeyboardButton(text='меню', callback_data='menu'))

# выбор решалы последний
keyboard14 = InlineKeyboardBuilder()
keyboard14.row(InlineKeyboardButton(text='◀️', callback_data='prev'),
               InlineKeyboardButton(text='Выбрать решалу', callback_data='gotovo'))
keyboard14.row(InlineKeyboardButton(text='меню', callback_data='menu'))

#отмена
keyboard15 = InlineKeyboardBuilder()
keyboard15.row(InlineKeyboardButton(text='Отмена', callback_data='otmena'))