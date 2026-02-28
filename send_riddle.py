import json
import requests
import sys
import os

# ──────────────────────────────────────────
# НАСТРОЙКИ — заполни перед запуском
# ──────────────────────────────────────────
BOT_TOKEN   = "8352461770:AAHOe1o5jghAwgByAaMoOc7TZn6I_i3swcI"      # токен от @BotFather
CHAT_ID     = "879672892"        # числовой ID пользователя

PHOTO_1     = "love.jpg"            # путь к первому фото
PHOTO_2     = "task.jpg"            # путь ко второму фото

MESSAGE     = "твоя последняя загадка"
# ──────────────────────────────────────────

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_media_group(photo1: str, photo2: str, caption: str) -> None:
    for path in (photo1, photo2):
        if not os.path.exists(path):
            print(f"Файл не найден: {path}", file=sys.stderr)
            sys.exit(1)

    url = f"{BASE_URL}/sendMediaGroup"
    media = [
        {"type": "photo", "media": "attach://photo1", "caption": caption},
        {"type": "photo", "media": "attach://photo2"},
    ]
    with open(photo1, "rb") as f1, open(photo2, "rb") as f2:
        resp = requests.post(
            url,
            data={"chat_id": CHAT_ID, "media": json.dumps(media)},
            files={"photo1": f1, "photo2": f2},
        )
    resp.raise_for_status()
    print("Альбом с подписью отправлен.")


def get_updates(offset: int) -> list:
    url = f"{BASE_URL}/getUpdates"
    resp = requests.get(url, params={"offset": offset, "timeout": 30}, timeout=35)
    resp.raise_for_status()
    return resp.json().get("result", [])


def wait_and_send() -> None:
    print("Бот запущен, жду сообщения...")
    offset = 0
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            sender_id = str(msg.get("chat", {}).get("id", ""))
            if sender_id == CHAT_ID:
                text = msg.get("text", "")
                print(f"Получено сообщение: {text!r}")
                send_media_group(PHOTO_1, PHOTO_2, MESSAGE)
                print("Готово.")
                sys.exit(0)


if __name__ == "__main__":
    wait_and_send()
