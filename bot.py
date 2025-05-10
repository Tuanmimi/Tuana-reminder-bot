# bot.py
import re
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-напоминалка.\n"
        "Напиши мне в таком формате:\n"
        "напомни [что сделать] в [ЧЧ:ММ]\n"
        "Пример: напомни позвонить маме в 18:00"
    )

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # Поиск шаблона: напомни ... в HH:MM
    match = re.search(r"напомни (.+) в (\d{1,2}:\d{2})", text)
    if not match:
        return  # Не напоминание — игнорируем

    reminder_text, time_str = match.group(1), match.group(2)

    try:
        target_time = datetime.strptime(time_str, "%H:%M").time()
        now = datetime.now()
        reminder_datetime = datetime.combine(now.date(), target_time)
        if reminder_datetime < now:
            reminder_datetime += timedelta(days=1)

        delay = (reminder_datetime - now).total_seconds()

        await update.message.reply_text(f"⏰ Напоминание установлено на {target_time.strftime('%H:%M')}")

        await asyncio.sleep(delay)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🔔 Напоминание: {reminder_text}")

    except ValueError:
        await update.message.reply_text("Ошибка: время должно быть в формате ЧЧ:ММ")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен... Жду сообщений")
    app.run_polling()

if __name__ == "__main__":
    main()
