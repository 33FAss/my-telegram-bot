import os
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = -1004334745848
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRAM_PDF_PATH = os.path.join(BASE_DIR, "program.pdf")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📋 ПОЛУЧИТЬ ПРОГРАММУ", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Привет! Раз ты здесь — что-то внутри уже откликнулось. Это не случайно ✨\n\n"
        "Пока я — бот Александра Синеркина, но помогу быстро связаться с нашей живой и дружной командой 🤗\n\n"
        "«Sinerkin Camp» — трансформационный ретрит с глубокой личной работой. Поэтому мы берём не всех (это правда): каждый участник проходит короткую диагностику, чтобы убедиться — действительно ли тебе подойдет программа.\n\n"
        "Нажми «ПОЛУЧИТЬ ПРОГРАММУ» — и мы передадим твой контакт специалисту по диагностике. Он свяжется, расскажет, что будет в лагере и что нужно, чтобы присоединиться 🙌",
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
        "Отлично, контакт получен! 🎉\n"
        "Программу ретрита можно посмотреть прямо сейчас:\n\n"
        "📁 На Яндекс Диске: https://disk.yandex.ru/i/nBn1F-yWPf1bsQ\n"
        "📁 На Google Диске: https://clck.ru/3UExgM\n\n"
        "Мы свяжемся с тобой в ближайшее время — проведём диагностику и честно скажем, подходит ли тебе этот формат.\n\n"
        "«Sinerkin Camp» — это 5 дней настоящей работы с собой. Не курс, не лекции. Живая трансформация.\n\n"
        "Если важно срочно написать — вот контакт продюсера: @bikkenina\n"
        "До встречи — возможно, уже в лагере! 😃",
        reply_markup=ReplyKeyboardRemove()
    )
    if os.path.exists(PROGRAM_PDF_PATH):
        await update.message.reply_document(
            document=InputFile(PROGRAM_PDF_PATH, filename="Sinerkin Camp — программа.pdf"),
            caption="📄 Sinerkin Camp — программа"
        )
    else:
        logging.error(f"PDF-файл не найден: {PROGRAM_PDF_PATH}")

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
