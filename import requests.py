import requests
import datetime

BOT_TOKEN = "5184976245:AAH_wrKxyC_oQonAw-yDcDt7C5nU48kHPBY"
CHAT_ID = "-1001657886690"
API_URL = "https://unired-mobile-api.cloudgate.uz/get_rate_marketing/"

def fetch_exchange_rates():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def format_message(data):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%d.%m.%Y %H:%M")
    message = f"🔔 <b>Курс {formatted_date}</b>\n\n"
    try:
        rub_to_uzs_sell = int(data[0]["buy"]) * 1000
        uzs_to_rub = float(data[0]["sell"]) * 1000
        usd_to_rub_visa = float(data[1]["sell"])

        message += (
            f"Россиядан - Узбекистонга 🇺🇿\n"
            f"<b>1000 RUB = {rub_to_uzs_sell} UZS</b>\n\n"
            f"Узбекистондан - Россияга 🇷🇺\n"
            f"<b>1000 RUB = {uzs_to_rub:.2f} UZS</b>\n\n"
            f"Россиядан - VISAга 💳\n"
            f"<b>1 $ = {usd_to_rub_visa:.2f} RUB</b>\n\n"
            f"Unired Mobile - Қулай пул ўтказмалар: <a href='https://onelink.to/unired_mobile'>юклаб олиш</a>\n\n"
            f"Илованинг расмий телеграм канали: <a href='http://t.me/uniredmobile'>@uniredmobile</a>\n\n"
            f"📞 Bizning telegram operatorimiz:\n"
            f"<a href='https://t.me/uniredmobile_bot'>@uniredmobile_bot</a>"
        )
        return message
    except Exception as e:
        print(f"Error formatting message: {e}")
        return "Error occurred"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Сообщение успешно отправлено в Telegram")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

def main():
    exchange_rates = fetch_exchange_rates()
    if exchange_rates:
        message = format_message(exchange_rates)
        send_telegram_message(message)

if __name__ == "__main__":
    main()
