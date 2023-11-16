import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token="6712372829:AAHzgNZVeT3Idg1iswSn5EZexyuLxjm_Tcw")
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Простая база данных
products_db = {
    1: {"title": "Iphone 15 pro max", "price": 3400},
    2: {"title": "Телефон Oneplus", "price": 1500},
    3: {"title": "Телефон Sony", "price": 300},
    4: {"title": "Iphone 14 pro", "price": 2600},
    5: {"title": "Телефон Huawei", "price": 500},
    6: {"title": "MacBook", "price": 3000},
    7: {"title": "Huawei Band 6", "price": 150},
    8: {"title": "Ноутбук Lenovo", "price": 1300},
    9: {"title": "Телевизор", "price": 1000},
    10: {"title": "Игровой компьютер", "price": 2500}
}

# Класс State, определяющий состояния
class Form(StatesGroup):
    product = State()

# Обработчик команды /start для отображения меню
@dp.message_handler(commands=['start'], state="*")
async def show_menu(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🛒 Показать товары')
    item2 = types.KeyboardButton('ℹ️ Информация')
    markup.add(item1, item2)
    await message.answer("Привет! Я бот. Чем могу помочь? Кликай по кнопком в зависимости от твоих желаний).", reply_markup=markup)

# Обработчик кнопки "Показать товары" в меню
@dp.message_handler(text='🛒 Показать товары', state="*")
async def process_show_products(message: types.Message):
    # Создаем Inline Keyboard для выбора товаров
    keyboard = types.InlineKeyboardMarkup()
    for product_id, product_info in products_db.items():
        button_text = f"{product_info['title']} - {product_info['price']} руб."
        callback_data = f'show_product_{product_id}'
        button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
        keyboard.add(button)
    await message.answer("Доступные товары:", reply_markup=keyboard)

# Обработчик нажатия на товар в списке
@dp.callback_query_handler(lambda query: query.data.startswith('show_product'), state="*")
async def process_show_product(callback_query: types.CallbackQuery):
    product_id = int(callback_query.data.split('_')[-1])
    product_info = products_db.get(product_id)
    await bot.send_message(callback_query.from_user.id, f"Товар: {product_info['title']}, Цена: {product_info['price']} руб.")

# Обработчик кнопки "ℹ️ Информация" в меню
@dp.message_handler(text='ℹ️ Информация', state="*")
async def process_information(message: types.Message):
    await message.answer("Это бот, который содержит товары и имитацию их покупок! Жми кнопку Показать товары, чтобы посмотреть все доступные товары.")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
