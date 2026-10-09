import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Вставь сюда токен своего бота от @BotFather
TOKEN = "8546728259:AAHUeYhCeoYGH5tslFNbvWXNsqUQM07PEbg"

# Список юзернеймов, которым разрешено запускать гарантированный рандом (без символа @)
ALLOWED_USERS = ["shuradzuki", "shiradzuki"]

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Глобальные переменные для отслеживания состояния режима /random1
is_random1_active = False
target_message_count = 0
current_message_count = 0


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет! Я бот-рандомайзер. Я слежу за чатом и случайно дарю валюту Грам!"
    )


@dp.message(Command("random1"))
async def random1_cmd(message: types.Message):
    global is_random1_active, target_message_count, current_message_count

    # Проверяем, задан ли username у пользователя
    username = message.from_user.username

    if username and username.lower() in [u.lower() for u in ALLOWED_USERS]:
        is_random1_active = True
        current_message_count = 0
        # Выбираем случайное сообщение от 1 до 10 среди следующих
        target_message_count = random.randint(1, 10)

        await message.reply(
            "✅ <b>Режим принудительного выбора активирован!</b>\n"
            "Победитель будет выбран в пределах следующих 10 сообщений.",
            parse_mode="HTML"
        )
    else:
        await message.reply("❌ У вас нет доступа к этой команде.")


@dp.message()
async def random_reward_handler(message: types.Message):
    global is_random1_active, target_message_count, current_message_count

    # Игнорируем сообщения от ботов и команды (начинающиеся с /)
    if message.from_user.is_bot or message.text.startswith("/"):
        return

    should_win = False

    # 1. Проверяем режим принудительного выбора /random1
    if is_random1_active:
        current_message_count += 1
        if current_message_count >= target_message_count:
            should_win = True
            is_random1_active = False  # Сбрасываем режим после выигрыша

    # 2. Если режим /random1 не активен, работает стандартный случайный шанс (0.25% = 1 из 400)
    elif random.randint(1, 400) == 1:
        should_win = True

    # Оформляем и отправляем выигрыш
    if should_win:
        amount = random.randint(100, 2000) * 100
        amount_formatted = f"{amount:,}".replace(",", " ")
        user_mention = message.from_user.mention_html()

        text = (
            f"🎉 <b>СЛУЧАЙНЫЙ ВЫИГРЫШ!</b>\n\n"
            f"Пользователь {user_mention} выиграл <b>{amount_formatted} Грам</b>!\n\n"
            f"Организатор: @shiradzuki"
        )

        await message.reply(text, parse_mode="HTML")


async def main():
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
