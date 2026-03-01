import os
import sys
from dotenv import load_dotenv
from telegram import InputMediaPhoto
from telegram.ext import Application, MessageHandler, filters

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
PHOTO_1   = os.environ["PHOTO_1"]
PHOTO_2   = os.environ["PHOTO_2"]
MESSAGE   = os.environ["MESSAGE"]


async def handle_message(update, context):
    if str(update.message.chat_id) != CHAT_ID:
        return

    print(f"Получено сообщение: {update.message.text!r}")

    with open(PHOTO_1, "rb") as f1, open(PHOTO_2, "rb") as f2:
        await context.bot.send_media_group(
            chat_id=CHAT_ID,
            media=[
                InputMediaPhoto(media=f1, caption=MESSAGE),
                InputMediaPhoto(media=f2),
            ],
        )

    print("Альбом отправлен. Завершаю работу.")
    context.application.stop_running()


def main():
    for path in (PHOTO_1, PHOTO_2):
        if not os.path.exists(path):
            print(f"Файл не найден: {path}", file=sys.stderr)
            sys.exit(1)

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Бот запущен, жду сообщения...")
    app.run_polling()


if __name__ == "__main__":
    main()
