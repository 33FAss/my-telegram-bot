import os
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = -1004334745848
PROGRAM_LINK = "https://disk.yandex.ru/i/YBnpsWvXX5NLRw"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRAM_PDF_PATH = os.path.join(BASE_DIR, "program.pdf")

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📋 ПОЛУЧИТЬ ПРОГРАММУ", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Приветствую! Пока я — бот, но я помогу тебе быстро связаться с нашей живой и дружной командой и получить необходимую информацию.\n\n"
        "Просто нажми «ПОЛУЧИТЬ ПРОГРАММУ», и мы переключим тебя на специалиста, который поможет записать тебя.",
        reply_markup=keyboard
    )


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user = update.message.from_user

    text = (
        f"📩 Новая заявка!\n"
        f"👤 Имя: {contact.first_name} {contact.last_name or ''}\n"
        f"📞 Телефон: {contact.phone_number}\n"
        f"🔗 Telegram: @{user.username or 'нет username'}\n"
        f"🆔 ID: {user.id}"
    )

    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=text)

    await update.message.reply_text(
        f"Спасибо! Программу можно посмотреть в приложенном документе или по ссылке:\n{PROGRAM_LINK}\n\nСвяжемся с вами в ближайшее время!",
        reply_markup=ReplyKeyboardRemove()
    )

    if os.path.exists(PROGRAM_PDF_PATH):
        with open(PROGRAM_PDF_PATH, "rb") as pdf:
    await update.message.reply_document(
        document=pdf,
        filename="Выход на свой путь.pdf",
        caption="📄 Выход на свой путь"
    )
    else:
        logging.error(f"PDF-файл не найден: {PROGRAM_PDF_PATH}")
        await update.message.reply_text(
            "PDF-файл временно недоступен, но программу можно посмотреть по ссылке выше."
        )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден. Проверь переменные окружения в Railway.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
