import io
from aiogram import Bot, Dispatcher, types
import asyncio
from PIL import Image

# Устанавливаем токен вашего бота
API_TOKEN = 'YOUR_BOT_TOKEN' # Сюда токен вашего бота

# Инициализируем бот и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def process_and_send_photo(photo: types.PhotoSize, bot: Bot, chat_id: int):
    # Получаем информацию о файле фотографии
    file_info = await bot.get_file(photo.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    # Открываем изображение с использованием Pillow
    image = Image.open(io.BytesIO(downloaded_file.read()))

    # Уменьшаем размер изображения в два раза
    resized_image = image.resize((image.width // 2, image.height // 2))

    # Обрезаем изображение в два раза
    cropped_image = resized_image.crop((0, 0, resized_image.width // 2, resized_image.height // 2))

    output = io.BytesIO()
    cropped_image.save(output, format='PNG')
    output.seek(0)

    # Отправляем уменьшенное и обрезанное изображение обратно пользователю
    await bot.send_photo(chat_id, photo=output)

    output.close()

# Обработчик для принятия фотографий и их уменьшения
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def process_photo(message: types.Message):
    # Получаем объект фотографии
    photo = message.photo[-1]
    await process_and_send_photo(photo, bot, message.chat.id)

# Отправка приветственного сообщения и информации о боте по команде /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот-обрезчик изображений. Просто отправь мне фотографию, и я уменьшу ее в два раза и отправлю тебе обратно!")

# Запускаем бота
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()
