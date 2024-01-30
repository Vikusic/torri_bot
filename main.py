from random import randint

from aiogram import Bot, Dispatcher
from aiogram import types
#from aiogram.dispatcher.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.dispatcher import router
from aiogram.handlers import MessageHandler
from aiogram.filters import Command

from config import TOKEN
from bd_connect import stroka, product_reseach

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

#----машина
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
#-----
bot = Bot(token=TOKEN)
# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()
dp = Dispatcher()

#машины состояний
# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_name = State()  # Состояние ожидания ввода имени
    fill_age = State()  # Состояние ожидания ввода возраста
    fill_type = State()  # Состояние ожидания выбора пола
    fill_aroma = State()  # Состояние ожидания загрузки фото
    fill_color = State()
    fill_wish_news = State()  # Состояние ожидания выбора получать ли новости




@dp.message(CommandStart())           #создаёт кнопочки
async def cmd_start(message: types.Message):
    button = [[types.KeyboardButton(text = 'учёт продуктов'),
            types.KeyboardButton(text = 'учёт материалов'),
            types.KeyboardButton(text='доход/расход')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard= button,resize_keyboard=True)
    await message.answer('Выберите категорию', reply_markup=keyboard)

@dp.message(F.text =='учёт продуктов')
async def but1(message: types.Message):
    await message.answer("*Вы выбрали учёт продуктов*", parse_mode="Markdown")
    button = [[types.KeyboardButton(text = 'Добавить продукт, /fillform'),
               types.KeyboardButton(text = 'Убрать продукт'),
               types.KeyboardButton(text='Вывести актуальный список')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard= True)
    await message.answer('Что хотите сделать?', reply_markup=keyboard)

# Этот хэндлер будет срабатывать на команду /fillform и переводить бота в состояние ожидания ввода названия
@dp.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите название')
    # Устанавливаем состояние ожидания ввода названия
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное название и переводить в состояние ожидания ввода веса
@dp.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное название в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите вес свечи')
    # Устанавливаем состояние ожидания ввода веса
    await state.set_state(FSMFillForm.fill_age)

# Этот хэндлер будет срабатывать, если введен корректный вес и переводить в состояние выбора категории
@dp.message(StateFilter(FSMFillForm.fill_age),
            lambda x: x.text.isdigit() and int(x.text) >= 5)
async def process_age_sent(message: Message, state: FSMContext):
    # Cохраняем вес в хранилище по ключу "age"
    await state.update_data(age=message.text)
    # Создаем объекты инлайн-кнопок
    candle_fig_button = InlineKeyboardButton(text='свеча контейнерная', callback_data='свеча контейнерная')
    candle_con_button = InlineKeyboardButton(text = 'свеча формовая', callback_data='свеча формовая')
    diff_button = InlineKeyboardButton(text='диффузор', callback_data='диффузор')
    sache_button = InlineKeyboardButton(text='саше', callback_data='саше')
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [[candle_fig_button], [candle_con_button], [diff_button],[sache_button]]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text='Спасибо!\n\nУкажите категорию', reply_markup=markup )
    # Устанавливаем состояние ожидания выбора категории
    await state.set_state(FSMFillForm.fill_type)

# Этот хэндлер будет срабатывать на нажатие кнопки при выборе категории и переводить в состояние отправки аромата
@dp.callback_query(StateFilter(FSMFillForm.fill_type),
                   F.data.in_(['свеча формовая','свеча контейнерная', 'диффузор', 'саше']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище, по ключу "type"
    await state.update_data(type=callback.data)

    if callback.data == 'свеча формовая':
        print('фигурка')
        await bot.send_message(1360095076, 'sxdcfyvgubh')
    else:
        print('------')
        await bot.send_message(1360095076, '------')
    # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото, чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(text='Спасибо! А теперь напишите используемый аромат')
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(FSMFillForm.fill_aroma)

# Этот хэндлер будет срабатывать, если отправлено аромат и переводить в состояние выбора цвета
@dp.message(StateFilter(FSMFillForm.fill_aroma), F.text.isalpha())
async def process_aroma_sent(message: Message, state: FSMContext):
    # Cохраняем введенное название в хранилище по ключу ""
    await state.update_data(aroma=message.text)
    await message.answer(text='Спасибо!')

    # Создаем объекты инлайн-кнопок
    violet_button = InlineKeyboardButton(text='фиолетовый', callback_data='Фиолетовый')
    blue_button = InlineKeyboardButton(text='бирюзовый', callback_data='Бирюзовый')
    no_color_button = InlineKeyboardButton(text='без цвета', callback_data='Без красителя')
    keyboard2: list[list[InlineKeyboardButton]] = [[violet_button], [blue_button], [no_color_button]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard2)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text='Спасибо!\n\nУкажите используемый цвет', reply_markup=markup)
    await state.set_state(FSMFillForm.fill_color)

@dp.message(StateFilter(FSMFillForm.fill_color), F.data.in_(['Фиолетовый','Бирюзовый','Без красителя']))
async  def process_color_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище, по ключу "type"
    await state.update_data(color=callback.data)
    await callback.message.delete()
    await callback.message.answer(text='Спасибо!')


    # Создаем объекты инлайн-кнопок
    yes_news_button = InlineKeyboardButton(
        text='Да',
        callback_data='yes_news'
    )
    no_news_button = InlineKeyboardButton(
        text='Нет, спасибо',
        callback_data='no_news')
    # Добавляем кнопки в клавиатуру в один ряд
    keyboard: list[list[InlineKeyboardButton]] = [
        [yes_news_button, no_news_button]
    ]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Редактируем предыдущее сообщение с кнопками, отправляя
    # новый текст и новую клавиатуру
    await Message.message.answer(text='Спасибо!\n\nОстался последний шаг.\nХотели бы вы получать новости?',reply_markup=markup)
    # Устанавливаем состояние ожидания выбора получать новости или нет
    await state.set_state(FSMFillForm.fill_wish_news)


# Этот хэндлер будет срабатывать на выбор получать или не получать новости и выводить из машины состояний
@dp.callback_query(StateFilter(FSMFillForm.fill_wish_news),
                   F.data.in_(['yes_news', 'no_news']))
async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные о получении новостей по ключу "wish_news"
    await state.update_data(wish_news=callback.data == 'yes_news')
    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    user_dict[callback.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    await state.clear()
    # Отправляем в чат сообщение о выходе из машины состояний
    await callback.message.edit_text(
        text='Спасибо! Ваши данные сохранены!\n\n'
             'Вы вышли из машины состояний'
    )
    # Отправляем в чат сообщение с предложением посмотреть свою анкету
    await callback.message.answer(
        text='Чтобы посмотреть данные вашей '
             'анкеты - отправьте команду /showdata'
    )


# Этот хэндлер будет срабатывать, если во время согласия на получение новостей будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_wish_news))
async def warning_not_wish_news(message: Message):
    await message.answer(
        text='Пожалуйста, воспользуйтесь кнопками!\n\nЕсли вы хотите прервать заполнение анкеты - отправьте команду /cancel')


# Этот хэндлер будет срабатывать на отправку команды /showdata и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@dp.message(Command(commands='showdata'), StateFilter(default_state))
async def process_showdata_command(message: Message):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    if message.from_user.id in user_dict:
        await message.answer_photo(
            photo=user_dict[message.from_user.id]['photo_id'],
            caption=f'Название: {user_dict[message.from_user.id]["name"]}\n'
                    f'Вес: {user_dict[message.from_user.id]["age"]}\n'
                    f'Категория: {user_dict[message.from_user.id]["type"]}\n'
                    f'Аромат: {user_dict[message.from_user.id]["aroma"]}\n'
                    f'Краситель: {user_dict[message.from_user.id]["color"]}\n'
                    f'Получать новости: {user_dict[message.from_user.id]["wish_news"]}'
        )
    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(
            text='Вы еще не заполняли анкету. Чтобы приступить - '
                 'отправьте команду /fillform'
        )






















@dp.message(F.text == 'учёт материалов')
async def but2(message: types.Message):
    await message.answer("*Вы выбрали учёт материалов*", parse_mode="Markdown")
    button = [[types.KeyboardButton(text='Добавить материалы'),
               types.KeyboardButton(text='Убрать материалы'),
               types.KeyboardButton(text ='Вывести список актуальных материалов')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer('Что хотите сделать?', reply_markup=keyboard)
@dp.message(F.text == 'доход/расход')
async def but3(message: types.Message):
    await message.answer("*Вы выбрали учёт доходов и расходов*", parse_mode="Markdown")
    button = [[types.KeyboardButton(text = 'Добавить расходы'),
               types.KeyboardButton(text = 'Добавить доходы'),
               types.KeyboardButton(text ='Вывести расходы и доходы')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard= True)
    await message.answer('Что хотите сделать?', reply_markup=keyboard)

# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fillform
@dp.message(Command('st'), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text='Этот бот демонстрирует работу FSM\n\n'
             'Чтобы перейти к заполнению анкеты - '
             'отправьте команду /fillform'
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне машины состояний\n\n'
             'Чтобы перейти к заполнению анкеты - '
             'отправьте команду /fillform'
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из машины состояний\n\n'
             'Чтобы снова перейти к заполнению анкеты - '
             'отправьте команду /fillform'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# # Этот хэндлер будет срабатывать на команду /fillform
# # и переводить бота в состояние ожидания ввода имени
# @dp.message(Command(commands='fillform'), StateFilter(default_state))
# async def process_fillform_command(message: Message, state: FSMContext):
#     await message.answer(text='Пожалуйста, введите ваше имя')
#     # Устанавливаем состояние ожидания ввода имени
#     await state.set_state(FSMFillForm.fill_name)


# # Этот хэндлер будет срабатывать, если введено корректное имя
# # и переводить в состояние ожидания ввода возраста
# @dp.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
# async def process_name_sent(message: Message, state: FSMContext):
#     # Cохраняем введенное имя в хранилище по ключу "name"
#     await state.update_data(name=message.text)
#     await message.answer(text='Спасибо!\n\nА теперь введите ваш возраст')
#     # Устанавливаем состояние ожидания ввода возраста
#     await state.set_state(FSMFillForm.fill_age)


# # Этот хэндлер будет срабатывать, если во время ввода имени
# # будет введено что-то некорректное
# @dp.message(StateFilter(FSMFillForm.fill_name))
# async def warning_not_name(message: Message):
#     await message.answer(
#         text='То, что вы отправили не похоже на имя\n\n'
#              'Пожалуйста, введите ваше имя\n\n'
#              'Если вы хотите прервать заполнение анкеты - '
#              'отправьте команду /cancel'
#     )


# # Этот хэндлер будет срабатывать, если введен корректный возраст
# # и переводить в состояние выбора пола
# @dp.message(StateFilter(FSMFillForm.fill_age),
#             lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
# async def process_age_sent(message: Message, state: FSMContext):
#     # Cохраняем возраст в хранилище по ключу "age"
#     await state.update_data(age=message.text)
#     # Создаем объекты инлайн-кнопок
#     candle_button = InlineKeyboardButton(
#         text='свеча',
#         callback_data='свеча'
#     )
#     diff_button = InlineKeyboardButton(
#         text='диффузор',
#         callback_data='диффузор'
#     )
#     sache_button = InlineKeyboardButton(
#         text='саше',
#         callback_data='саше'
#     )
#     # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
#     keyboard: list[list[InlineKeyboardButton]] = [
#         [candle_button, diff_button],
#         [sache_button]
#     ]
#     # Создаем объект инлайн-клавиатуры
#     markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
#     # Отправляем пользователю сообщение с клавиатурой
#     await message.answer(
#         text='Спасибо!\n\nУкажите категорию',
#         reply_markup=markup
#     )
#     # Устанавливаем состояние ожидания выбора пола
#     await state.set_state(FSMFillForm.fill_type)
#
#
# # Этот хэндлер будет срабатывать, если во время ввода возраста
# # будет введено что-то некорректное
# @dp.message(StateFilter(FSMFillForm.fill_age))
# async def warning_not_age(message: Message):
#     await message.answer(
#         text='Возраст должен быть целым числом от 4 до 120\n\n'
#              'Попробуйте еще раз\n\nЕсли вы хотите прервать '
#              'заполнение анкеты - отправьте команду /cancel'
#     )


# # Этот хэндлер будет срабатывать на нажатие кнопки при
# # выборе пола и переводить в состояние отправки фото
# @dp.callback_query(StateFilter(FSMFillForm.fill_type),
#                    F.data.in_(['свеча', 'диффузор', 'саше']))
# async def process_gender_press(callback: CallbackQuery, state: FSMContext):
#     # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
#     # по ключу "type"
#     await state.update_data(type=callback.data)
#     # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
#     # чтобы у пользователя не было желания тыкать кнопки
#     await callback.message.delete()
#     await callback.message.answer(
#         text='Спасибо! А теперь загрузите, пожалуйста, ваше фото'
#     )
#     # Устанавливаем состояние ожидания загрузки фото
#     await state.set_state(FSMFillForm.upload_photo)
#
#
# # Этот хэндлер будет срабатывать, если во время выбора пола
# # будет введено/отправлено что-то некорректное
# @dp.message(StateFilter(FSMFillForm.fill_type))
# async def warning_not_gender(message: Message):
#     await message.answer(
#         text='Пожалуйста, пользуйтесь кнопками '
#              'при выборе пола\n\nЕсли вы хотите прервать '
#              'заполнение анкеты - отправьте команду /cancel'
#     )


# # Этот хэндлер будет срабатывать, если отправлено фото
# # и переводить в состояние выбора образования
# #foto -> edu
# @dp.message(StateFilter(FSMFillForm.upload_photo),
#             F.photo[-1].as_('largest_photo'))
# async def process_photo_sent(message: Message,
#                              state: FSMContext,
#                              largest_photo: PhotoSize):
#     await state.update_data(
#         photo_unique_id=largest_photo.file_unique_id,
#         photo_id=largest_photo.file_id)
#     # Создаем объекты инлайн-кнопок
#     yes_news_button = InlineKeyboardButton(
#         text='Да',
#         callback_data='yes_news'
#     )
#     no_news_button = InlineKeyboardButton(
#         text='Нет, спасибо',
#         callback_data='no_news')
#     # Добавляем кнопки в клавиатуру в один ряд
#     keyboard: list[list[InlineKeyboardButton]] = [
#         [yes_news_button, no_news_button]
#     ]
#     # Создаем объект инлайн-клавиатуры
#     markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
#     # Редактируем предыдущее сообщение с кнопками, отправляя
#     # новый текст и новую клавиатуру
#     await message.answer(
#         text='Спасибо!\n\nОстался последний шаг.\n'
#              'Хотели бы вы получать новости?',
#         reply_markup=markup
#     )
#     # Устанавливаем состояние ожидания выбора получать новости или нет
#     await state.set_state(FSMFillForm.fill_wish_news)
#
#
# # Этот хэндлер будет срабатывать, если во время отправки фото
# # будет введено/отправлено что-то некорректное
# @dp.message(StateFilter(FSMFillForm.upload_photo))
# async def warning_not_photo(message: Message):
#     await message.answer(
#         text='Пожалуйста, на этом шаге отправьте '
#              'ваше фото\n\nЕсли вы хотите прервать '
#              'заполнение анкеты - отправьте команду /cancel'
#     )

#
# # Этот хэндлер будет срабатывать на выбор получать или
# # не получать новости и выводить из машины состояний
# @dp.callback_query(StateFilter(FSMFillForm.fill_wish_news),
#                    F.data.in_(['yes_news', 'no_news']))
# async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
#     # Cохраняем данные о получении новостей по ключу "wish_news"
#     await state.update_data(wish_news=callback.data == 'yes_news')
#     # Добавляем в "базу данных" анкету пользователя
#     # по ключу id пользователя
#     user_dict[callback.from_user.id] = await state.get_data()
#     # Завершаем машину состояний
#     await state.clear()
#     # Отправляем в чат сообщение о выходе из машины состояний
#     await callback.message.edit_text(
#         text='Спасибо! Ваши данные сохранены!\n\n'
#              'Вы вышли из машины состояний'
#     )
#     # Отправляем в чат сообщение с предложением посмотреть свою анкету
#     await callback.message.answer(
#         text='Чтобы посмотреть данные вашей '
#              'анкеты - отправьте команду /showdata'
#     )
#
#
# # Этот хэндлер будет срабатывать, если во время согласия на получение
# # новостей будет введено/отправлено что-то некорректное
# @dp.message(StateFilter(FSMFillForm.fill_wish_news))
# async def warning_not_wish_news(message: Message):
#     await message.answer(
#         text='Пожалуйста, воспользуйтесь кнопками!\n\n'
#              'Если вы хотите прервать заполнение анкеты - '
#              'отправьте команду /cancel'
#     )
#
#
# # Этот хэндлер будет срабатывать на отправку команды /showdata
# # и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
# @dp.message(Command(commands='showdata'), StateFilter(default_state))
# async def process_showdata_command(message: Message):
#     # Отправляем пользователю анкету, если она есть в "базе данных"
#     if message.from_user.id in user_dict:
#         await message.answer_photo(
#             photo=user_dict[message.from_user.id]['photo_id'],
#             caption=f'Имя: {user_dict[message.from_user.id]["name"]}\n'
#                     f'Возраст: {user_dict[message.from_user.id]["age"]}\n'
#                     f'Категория: {user_dict[message.from_user.id]["type"]}\n'
#                     f'Получать новости: {user_dict[message.from_user.id]["wish_news"]}'
#         )
#     else:
#         # Если анкеты пользователя в базе нет - предлагаем заполнить
#         await message.answer(
#             text='Вы еще не заполняли анкету. Чтобы приступить - '
#                  'отправьте команду /fillform'
#         )


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
#/////
# @dp.message(StateFilter(default_state))
# async def send_echo(message: Message):
#     await message.reply(text='Извините, моя твоя не понимать')


#------------------------------------------------
# Если не указать фильтр F.text,  то хэндлер сработает даже на картинку с подписью /test
# @dp.message(F.text, Command("test"))
# async def any_message(message: Message):
#     await message.answer(
#         "Hello, <b>world</b>!",
#         parse_mode=ParseMode.HTML
#     )
#     await message.answer(
#         "Hello, *world*\!",
#         parse_mode=ParseMode.MARKDOWN_V2
#     )
@dp.message(Command('send'))
async def send_message(message: types.Message):
    print(message.model_dump_json(indent=4, exclude_none=True))
    await bot.send_message(422611492, 'Хыыыыыыыыыы')



@dp.message(F.text, Command("start"))     #в версии 3. messgae_handler == message
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message(Command('help'))
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")

# @dp.message()
# async def send_echo(message: types.Message):
#     await message.reply(text=message.text)



#-----------------------------b---o---t---------------
@dp.message(Command('candle'))           #создаёт кнопочки
async def cmd_start(message: types.Message):
    button = [[types.KeyboardButton(text = 'свечи'),
            types.KeyboardButton(text = 'диффузоры'),
            types.KeyboardButton(text='саше')],
            types.KeyboardButton(text='Добавить продукт')]
    keyboard = types.ReplyKeyboardMarkup(keyboard= button,resize_keyboard=True,input_fieled = 'Выбери категорию')
    await message.answer('Категория', reply_markup=keyboard)
@dp.message(F.text =='свечи')
async def but1(message: types.Message):
    await message.reply(("*Свечи: \n*") + product_reseach(1), parse_mode="Markdown")
@dp.message(F.text == 'диффузоры')
async def but2(message: types.Message):
  await message.reply("*Диффузоры: \n*" + product_reseach(2), parse_mode="Markdown")
@dp.message(F.text == 'саше')
async def but3(message: types.Message):
    await message.reply("*Саше: \n*" + product_reseach(3), parse_mode="Markdown")

@dp.message(F.text == 'Добавить продукт')
async def but4(message: types.Message):
    await message.reply("*Саше: \n*" + product_reseach(3), parse_mode="Markdown")




# Создаем объекты инлайн-кнопок
add_button = InlineKeyboardButton(
    text='Добавить товар',
    callback_data='add_product_press'
)
update_button = InlineKeyboardButton(
    text='Изменить товар',
    callback_data='update_product_press'
)
delete_button = InlineKeyboardButton(
    text = 'Удалить товар',
    callback_data='delete_product_press'
)
# Создаем объект инлайн-клавиатуры
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[add_button],
                     [update_button],
                     [delete_button]]
)
# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру с инлайн-кнопками
@dp.message(Command('product'))
async def process_start_command(message: types.Message):
    await message.answer(
        text='Выбери опцию',
        reply_markup=keyboard
)

# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_1_pressed'
@dp.callback_query(F.data == 'add_product_press')
async def add_product_press(callback: CallbackQuery):
    if callback.message.text != 'Добавить товар':
        await callback.message.edit_text(
            text='Добавить товар',
            reply_markup=callback.message.reply_markup
        )
    @dp.message()
    async def send_sms(message: types.Message):
        text1 = message.text
        await message.answer(text='Добавить '+ text1 + ' :)?')
        if message.text == 'да':
            await message.answer(text = 'Готово!')
        else:
            await message.answer(text='Отмена!')
    await callback.answer()


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_2_pressed'
@dp.callback_query(F.data == 'update_product_press')
async def update_product_press(callback: CallbackQuery):
    if callback.message.text != 'Изменить товар':
        await callback.message.edit_text(
            text='Изменить товар',
            reply_markup=callback.message.reply_markup
        )
    await callback.answer()

@dp.callback_query(F.data == 'delete_product_press')
async def delete_product_press(callback: CallbackQuery):
    if callback.message.text != 'Удалить товар':
        await callback.message.edit_text(
            text = 'Удалить товар',
            reply_markup= callback.message.reply_markup
        )
    await callback.answer()



# inline_btn_1 = InlineKeyboardButton('Третья кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
# # Создаем объекты инлайн-кнопок
# button_inline_4 = InlineKeyboardButton(text='кнопка 4',callback_data='button_4_pressed')
# button_inline_5 = InlineKeyboardButton(text='кнопка 5',callback_data='button_5_pressed')
# # Создаем объект инлайн-клавиатуры
# keyboard4 = InlineKeyboardMarkup(inline_keyboard=[[button_inline_4],[button_inline_5]])
#
# # Этот хэндлер будет срабатывать на команду "/start1" и отправлять в чат клавиатуру с инлайн-кнопками
# @dp.message(Command('2'))
# async def process_end_command(message: types.Message):
#     await message.answer(text='Это инлайн-кнопки. Нажми на любую!',reply_markup=keyboard4)
#
#
# # Этот хэндлер будет срабатывать на апдейт типа CallbackQuery с data 'button_4_pressed' или 'button_5_pressed'
# @dp.callback_query(F.data.in_(['button_4_pressed', 'button_5_pressed']))
# async def process_buttons_press(callback: CallbackQuery):
#     await callback.answer()

#(#для 3 версии
@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Нажми меня",callback_data="random_value"))
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10",reply_markup=builder.as_markup())

@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
#)



# @dp.message_handler(commands=['1'])
# async def but3(message: types.Message):
#     await message.reply("Кнопка 3", reply_markup=InlineKeyboardMarkup().add(inline_btn_1))
#
# # @dp.callback_query_handler(lambda call: True) #: c.data == 'Третья кнопка')   #рабочий вариант
# # async def answer(call): #(callback_query: types.CallbackQuery):
# #     if call.data == 'Третья кнопка':
# #         #await bot.answer_callback_query(callback_query.id)
# #         await bot.send_message(call.message.from_user.id, 'Нажата третья кнопка!')
# #
# @dp.callback_query_handler(text='Третья кнопка!')   #оже рабочий вариант
# async def inlines(callback: types.CallbackQuery):
#     await bot.send_message(callback.message.from_user.id, 'Нажата третья кнопка!')








# @dp.callback_query_handler(func=lambda c: c.data == 'button1')
# async def process_callback_button1(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
#



# # @dp.message_handler(content_types=[types.ContentType.ANIMATION])
# # async def echo_document(message: types.Message):
# #     #id = CgACAgQAAxkBAAOlZO9LSc0E93EtPhQ8MNnKWWfZttgAAt0CAAKxYg1TPQnHKFXuA_MwBA
# #     await message.reply_animation(message.animation.file_id)
# #  #os.listdir(peth = "")
# #     print(message.animation.file_id)
#
# @dp.message_handler(commands = ['k'])
# async def echo_document(message: types.Message):
#     file_id =" CgACAgQAAxkBAAOlZO9LSc0E93EtPhQ8MNnKWWfZttgAAt0CAAKxYg1TPQnHKFXuA_MwBA"
#     await message.reply_animation(file_id)
#  #os.listdir(peth = "")
#     print(message.animation.file_id)
#
# # @dp.message_handler(content_types=[types.ContentType.PHOTO])
# # async def echo_photo(message: types.Message):
# #     await bot.send_photo(msg.from_user.id, msg.photo)










# Регистрируем хэндлеры
dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))


if __name__ == '__main__':
    dp.run_polling(bot)  #version 3.2.0
    #executor.start_polling(dp) versia2.25.1