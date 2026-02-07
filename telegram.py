import requests

# ========== TELEGRAM CONFIG ==========
 
BOT_TOKEN = "replace it with yoir chat token"
CHAT_ID = "replace with your chat id"

# ====================================

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

def send_photo(image_path, caption=None):
    data = {"chat_id": CHAT_ID}
    if caption:
        data["caption"] = caption

    with open(image_path, "rb") as photo:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data=data,
            files={"photo": photo}
        )
