import datetime
import os
import random
import requests

CITY = "Delhi"
COUNTRY_CODE = "IN"

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "8zb140d8859e21c72d5d5956ecd2175")
HOLIDAY_API_KEY = os.getenv("HOLIDAY_API_KEY", "EtGpkue87chwT7BPmPTUffxr5yqBfUrp")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8706649605:AAFOdAerAWQ7E3vuB9gM93tq7-fpS5qFBRc")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "6125641152")

STUDY_QUESTIONS = [
    {
        "topic": "SQL",
        "question": "WHERE aur HAVING clause me kya antar hai?",
        "answer": "WHERE aggregates se pehle rows filter karta hai, HAVING clause GROUP BY ke baad filter karta hai."
    },
    {
        "topic": "Python",
        "question": "Python me list aur tuple me kya antar hai?",
        "answer": "List Mutable hoti hai [], jabki Tuple Immutable hota hai ()."
    },
    {
        "topic": "SQL",
        "question": "PRIMARY KEY aur UNIQUE KEY me kya antar hai?",
        "answer": "Primary Key me NULL nahi ho sakta, Unique Key ek NULL allow karti hai."
    },
    {
        "topic": "Data Analytics",
        "question": "Mean, Median aur Mode kya hain?",
        "answer": "Mean average hai, Median middle value hai, Mode sabse zyada baar aane wala value hai."
    }
]

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            return f"{temp}°C, {desc}"
        return "Weather data unavailable"
    except Exception as e:
        return f"Weather error: {e}"

def get_occasion(country, api_key):
    today = datetime.date.today()
    url = f"https://calendarific.com/api/v2/holidays?api_key={api_key}&country={country}&year={today.year}&day={today.day}&month={today.month}"
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        holidays = data.get("response", {}).get("holidays", [])
        if holidays:
            names = [h["name"] for h in holidays]
            return ", ".join(names)
        return "No public holiday today"
    except Exception as e:
        return f"Holiday error: {e}"

def get_daily_question():
    q = random.choice(STUDY_QUESTIONS)
    return "📌 [{0}] {1}\n💡 Ans: {2}".format(q['topic'], q['question'], q['answer'])

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        res = requests.post(url, json=payload, timeout=30)
        print("Telegram Response Status:", res.status_code)
        print("Telegram Response Text:", res.text)
    except Exception as e:
        print(f"Error sending message: {e}")

def main():
    today_str = datetime.date.today().strftime("%A, %B %d, %Y")
    weather_info = get_weather(CITY, WEATHER_API_KEY)
    occasion_info = get_occasion(COUNTRY_CODE, HOLIDAY_API_KEY)
    q_text = get_daily_question()

    lines = [
        "📅 DAILY BRIEFING: " + today_str,
        "",
        "🌤 Weather (" + CITY + "): " + weather_info,
        "🎉 Occasion/Holiday: " + occasion_info,
        "",
        "🧠 QUESTION OF THE DAY:",
        q_text
    ]
    
    briefing = "\n".join(lines)

    print("--- GENERATED BRIEFING ---")
    print(briefing)
    print("--------------------------")
    
    send_telegram_message(briefing)

if __name__ == "__main__":
    main()
