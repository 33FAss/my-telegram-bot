import os
import logging
from pathlib import Path

from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InputFile,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.error import TelegramError


BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = -1004334745848
BASE_DIR = Path(__file__).resolve().parent
PROGRAM_PDF_PATH = BASE_DIR / "SinerkinCamp.pdf"

YANDEX_DISK_URL = "https://disk.yandex.ru/i/CuJld5ssmjZZSQ"
GOOGLE_DISK_URL = "https://clck.ru/3UHto7"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def is_pdf_ok(path: Path) -> bool:
    if not path.is_file():
        logging.error(f"PDF-файл не найден: {path}")
        return False

    if path.stat().st_size == 0:
        logging.error(f"PDF-файл пустой: {path}")
        return False

    with path.open("rb") as file:
        header = file.read(5)

    if header != b"%PDF-":
        logging.error(f"Файл не похож на PDF: {path}")
        return False

    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton(
        "📋 ПОЛУЧИТЬ ПРОГРАММУ",
        request_contact=True
    )

    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "Привет! Раз ты здесь — что-то внутри уже откликнулось. Это не случайно ✨\n\n"
        "Пока я — бот Александра Синеркина, но помогу быстро связаться с нашей живой и дружной командой 🤗\n\n"
        "«Sinerkin Camp» — трансформационный ретрит с глубокой личной работой. Поэтому мы берём не всех (это правда): каждый участник проходит короткую диагностику, чтобы убедиться — действительно ли тебе подойдет программа.\n\n"
        "Нажми «ПОЛУЧИТЬ ПРОГРАММУ» — и мы передадим твой контакт специалисту по диагностике. Он свяжется, расскажет, что будет в лагере и что нужно, чтобы присоединиться 🙌",
        reply_markup=keyboard
    )


async def send_program_pdf(update: Update):
    if not is_pdf_ok(PROGRAM_PDF_PATH):
        await update.message.reply_text(
            "PDF сейчас можно открыть по ссылкам:\n\n"
            f"📁 На Яндекс Диске: {YANDEX_DISK_URL}\n"
            f"📁 На Google Диске: {GOOGLE_DISK_URL}"
        )
        return

    try:
        with PROGRAM_PDF_PATH.open("rb") as pdf_file:
            await update.message.reply_document(
                document=InputFile(pdf_file, filename="SinerkinCamp.pdf")
            )

        logging.info(
            f"PDF успешно отправлен: {PROGRAM_PDF_PATH}, "
            f"размер: {PROGRAM_PDF_PATH.stat().st_size} байт"
        )

    except TelegramError as error:
        logging.exception(f"Ошибка Telegram при отправке PDF: {error}")

        await update.message.reply_text(
            "Не получилось отправить PDF файлом, но программу можно открыть по ссылкам:\n\n"
            f"📁 На Яндекс Диске: {YANDEX_DISK_URL}\n"
            f"📁 На Google Диске: {GOOGLE_DISK_URL}"
        )


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user = update.message.from_user

    application_text = (
        f"📩 Новая заявка!\n"
        f"👤 Имя: {contact.first_name} {contact.last_name or ''}\n"
        f"📞 Телефон: {contact.phone_number}\n"
        f"🔗 Telegram: @{user.username or 'нет username'}\n"
        f"🆔 ID: {user.id}"
    )

    try:
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=application_text
        )
    except TelegramError as error:
        logging.exception(f"Не получилось отправить заявку в группу: {error}")

    await update.message.reply_text(
        "Спасибо! Программу ретрита можно посмотреть файлом ниже или по ссылкам:\n\n"
        f"📁 На Яндекс Диске: {YANDEX_DISK_URL}\n"
        f"📁 На Google Диске: {GOOGLE_DISK_URL}\n\n"
        "Мы свяжемся с тобой в ближайшее время — проведём диагностику и честно скажем, подходит ли тебе этот формат.\n\n"
        "«Sinerkin Camp» — это 5 дней настоящей работы с собой. Не курс, не лекции. Живая трансформация.\n\n"
        "Если важно срочно написать или не открывается программа — вот контакт продюсера: @bikkenina\n"
        "До встречи — возможно, уже в лагере! 😃",
        reply_markup=ReplyKeyboardRemove()
    )

    await send_program_pdf(update)


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден. Проверь переменные окружения в Railway.")

    if not PROGRAM_PDF_PATH.exists():
        logging.warning(f"PDF-файл пока не найден: {PROGRAM_PDF_PATH}")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
