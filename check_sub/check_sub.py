import requests
from config.config import TOKEN, Chanel_id

CHANNEL_ID = Chanel_id

def check_sub(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember"
    
    params = {
        "chat_id": CHANNEL_ID,
        "user_id": chat_id
    }

    response = requests.get(url, params=params).json()

    status = response.get("result", {}).get("status")

    return status in ["member", "administrator", "creator"]