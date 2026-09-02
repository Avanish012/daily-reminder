import datetime
import requests

# --- कॉन्फ़िगरेशन ---
CITY = "Delhi"
COUNTRY_CODE = "IN"

WEATHER_API_KEY = "82b140d8859e21c72d5d59566ecd2175"
HOLIDAY_API_KEY = "EtGpkue87chwT7BPmPTUffxr5yqBfUrP"
TELEGRAM_TOKEN = "8706649605:AAFOdAerAWQ7E3vuB9gM93tq7-fpS5qFBRc"
TELEGRAM_CHAT_ID = "6125641152"


def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            return f"{temp}°C, {desc}"
        return "मौसम डेटा उपलब्ध नहीं है"
    except Exception as e:
        return f"त्रुटि: {e}"


def get_occasion(country, api_key):
    today = datetime.date.today()
    url = f"https://calendarific.com/api/v2/holidays?api_key={api_key}&country={country}&year={today.year}&day={today.day}&month={today.month}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        holidays = data.get("response", {}).get("holidays", [])
        if holidays:
            names = [h["name"] for h in holidays]
            return ", ".join(names)
        return "आज कोई मुख्य सार्वजनिक अवकाश नहीं है"
    except Exception as e:
        return f"त्रुटि: {e}"


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload, timeout=10)


def main():
    today_str = datetime.date.today().strftime("%A, %B %d, %Y")
    weather_info = get_weather(CITY, WEATHER_API_KEY)
    occasion_info = get_occasion(COUNTRY_CODE, HOLIDAY_API_KEY)

    briefing = (
        f"📅 DAILY BRIEFING: {today_str}\n\n"
        f"🌤 Weather ({CITY}): {weather_info}\n"
        f"🎉 Occasion/Holiday: {occasion_info}"
    )

    send_telegram_message(briefing)


if __name__ == "__main__":
    main()
