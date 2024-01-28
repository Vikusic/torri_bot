from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = 'BOT TOKEN HERE'

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=storage)

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_name = State()        # Состояние ожидания ввода имени
    fill_age = State()         # Состояние ожидания ввода возраста
    fill_gender = State()      # Состояние ожидания выбора пола
    upload_photo = State()     # Состояние ожидания загрузки фото
    fill_wish_news = State()   # Состояние ожидания выбора получать ли новости



# Этот хэндлер будет срабатывать, если отправлено фото
# и переводить в состояние выбора образования
#foto -> edu
@dp.message(StateFilter(FSMFillForm.upload_photo),
            F.photo[-1].as_('largest_photo'))
async def process_photo_sent(message: Message,
                             state: FSMContext,
                             largest_photo: PhotoSize):
    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id)
    # # Создаем объекты инлайн-кнопок
    # secondary_button = InlineKeyboardButton(
    #     text='Среднее',
    #     callback_data='secondary'
    # )
    # higher_button = InlineKeyboardButton(
    #     text='Высшее',
    #     callback_data='higher'
    # )
    # no_edu_button = InlineKeyboardButton(
    #     text='🤷 Нету',
    #     callback_data='no_edu'
    # )
    # # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    # keyboard: list[list[InlineKeyboardButton]] = [
    #     [secondary_button, higher_button],
    #     [no_edu_button]
    # ]
    # # Создаем объект инлайн-клавиатуры
    # markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # # Отправляем пользователю сообщение с клавиатурой
    # await message.answer(
    #     text='Спасибо!\n\nУкажите ваше образование',
    #     reply_markup=markup
    # )
    # # Устанавливаем состояние ожидания выбора образования
    # await state.set_state(FSMFillForm.fill_education)
# Этот хэндлер будет срабатывать, если выбрано образование
# и переводить в состояние согласия получать новости
#edu -> news
# @dp.callback_query(StateFilter(FSMFillForm.fill_education),
#                    F.data.in_(['secondary', 'higher', 'no_edu']))
# async def process_education_press(callback: CallbackQuery, state: FSMContext):
#     # # Cохраняем данные об образовании по ключу "education"
#     # await state.update_data(education=callback.data)




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
    await message.answer(
        text='Спасибо!\n\nОстался последний шаг.\n'
             'Хотели бы вы получать новости?',
        reply_markup=markup
    )
    # Устанавливаем состояние ожидания выбора получать новости или нет
    await state.set_state(FSMFillForm.fill_wish_news)








