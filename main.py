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


bot = Bot(token=TOKEN)
dp = Dispatcher()



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
@dp.message(F.text, Command("start"))     #в версии 3. messgae_handler == message
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message(Command('help'))
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


# @dp.message_handler()
# async def echo_message(msg: types.Message):
#      await bot.send_message(msg.from_user.id, msg.text)


@dp.message(Command('pogoda'))
async def pogoda_command(message: types.Message):
    await message.reply("Погода сегодня хорошая")

@dp.message(Command('baza'))
async def baza_command(message: types.Message):
    await message.reply(stroka())

@dp.message(Command('start1'))           #создаёт кнопочки
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True) #меньшает кнопочки, озвращает обратно к клавиутуре)
    buttons = ['кнопочка 1', 'кнопочка 2']
    keyboard.add(*buttons) #*-ля распаковки списка, а каждый add создает новую строку
    await message.answer("Это мои кнопочки", reply_markup = keyboard)



@dp.message(F.text =='кнопочка 1')
async def but1(message: types.Message):
    await message.reply("Хыыыыыы")

@dp.message(F.text == 'кнопочка 2')
async def but2(message: types.Message):
    await message.reply("Хиииии")

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


# #----------------
# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
#
# @dp.message_handler(commands=['1'])
# async def process_command_1(message: types.Message):
#     await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb1)
#





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


if __name__ == '__main__':
    dp.run_polling(bot)  #version 3.2.0
    #executor.start_polling(dp) versia2.25.1