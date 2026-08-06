import requests
import os


def send_message(text):

    token = os.environ.get(
        "TELEGRAM_TOKEN"
    )

    chat_id = os.environ.get(
        "TELEGRAM_CHAT_ID"
    )


    url = (
        f"https://api.telegram.org/"
        f"bot{token}/sendMessage"
    )


    data = {
        "chat_id": chat_id,
        "text": text
    }


    response = requests.post(
        url,
        data=data
    )


    response.raise_for_status()



if __name__ == "__main__":

    send_message(
        "🛡 Daily Security OSINT\n\n"
        "Telegram test úspěšný."
    )
