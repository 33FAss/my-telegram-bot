import os
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = -1004334745848
PROGRAM_LINK = "https://drive.google.com/file/d/1Zn2ffaI5Z3tS-wjJzJd7JTnBmNNh7yIs/view?usp=sharing"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📋 ПОЛУЧИТЬ ПРОГРАММУ", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Приветствую! Пока я — бот, но я помогу тебе быстро связаться с нашей живой и дружной командой и получить необходимую информацию.\n\nПросто нажми «ПОЛУЧИТЬ ПРОГРАММУ», и мы переключим тебя на специалиста, который поможет записать тебя.",
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
        f"Спасибо! Программу можно посмотреть тут:\n{PROGRAM_LINK}\n\nСвяжемся с вами в ближайшее время!",
        reply_markup=ReplyKeyboardRemove()
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
