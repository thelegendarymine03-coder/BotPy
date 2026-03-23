import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Токен из переменной среды
TOKEN = os.environ.get("TOKEN") or "8714445271:AAFCDMbVI7d6maMhPHPnG1L-57tPtWtfLuo"

# Список каналов для проверки подписки
REQUIRED_CHANNELS = ["@kanaldlypro"]

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    bot = context.bot

    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["left", "kicked"]:
                await bot.send_message(chat_id=chat_id, text=f"Ты не подписан на {channel}. Подпишись и напиши снова!")
                return
        except:
            await bot.send_message(chat_id=chat_id, text=f"Не могу проверить {channel}. Убедись, что бот админ в канале!")
            return

    await bot.send_message(chat_id=chat_id, text="Доступ есть! Можешь писать сообщения.")

# Создаём приложение (новый способ вместо Updater)
app = ApplicationBuilder().token(TOKEN).build()

# Обработчик всех текстовых сообщений
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_subscription))

# Запуск бота
app.run_polling()