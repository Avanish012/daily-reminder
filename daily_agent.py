import datetime
import requests

# --- कॉन्फ़िगरेशन ---
CITY = "Delhi"
COUNTRY_CODE = "IN"

WEATHER_API_KEY = "8zb140d8859e21c72d5d5956ecd2175"  # अपनी OpenWeather Key
HOLIDAY_API_KEY = "EtGpkue87chwT7BPmPTUffxr5yqBfUrp"  # अपनी Calendarific Key
TELEGRAM_TOKEN = "8706649605:AAFOdAerAWQ7E3vuB9gM93tq7-fpS5qFBRc"          # अपना Telegram Bot Token
TELEGRAM_CHAT_ID = "6125641152"          # अपनी Telegram Chat ID


def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            return f"{temp}°C, {desc}"
        return f"मौसम डेटा उपलब्ध नहीं है (Error: {data.get('message', 'Unknown')})"
    except Exception as e:
        return f"मौसम नेटवर्क एरर: {e}"


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
        return "आज कोई मुख्य सार्वजनिक अवकाश नहीं है"
    except Exception as e:
        return f"त्यौहार नेटवर्क एरर: {e}"
import random

# Data Analytics, Python और SQL का Question Bank
STUDY_QUESTIONS = [
    {
        "topic": "SQL",
        "question": "WHERE और HAVING clause में क्या अंतर है?",
        "answer": "WHERE क्लॉज़ aggregates से पहले पंक्तियों (rows) को फ़िल्टर करता है, जबकि HAVING क्लॉज़ GROUP BY के बाद aggregate रिजल्ट्स को फ़िल्टर करता है।"
    },
    {
        "topic": "Python",
        "question": "Python में list और tuple के बीच मुख्य अंतर क्या है?",
        "answer": "List Mutable (परिवर्तनशील) होती है और इसे वर्गाकार कोष्ठक [] से बनाया जाता है, जबकि Tuple Immutable (अपरिवर्तनीय) होता है और () से बनाया जाता है।"
    },
    {
        "topic": "SQL",
        "question": "PRIMARY KEY और UNIQUE KEY में मुख्य अंतर क्या है?",
        "answer": "Primary Key टेबल में हर रिकॉर्ड को विशिष्ट रूप से पहचानती है और इसमें NULL मान नहीं हो सकता। Unique Key भी यूनिक मान सुनिश्चित करती है लेकिन एक NULL वैल्यू की अनुमति देती है।"
    },
    {
        "topic": "Data Analytics",
        "question": "Data Analytics में Mean, Median और Mode में क्या अंतर है?",
        "answer": "Mean औसत मान है, Median डेटासेट का मध्य मान है, और Mode वह मान है जो सबसे अधिक बार दोहराया जाता है।"
    },
    {
        "topic": "Python",
        "question": "Python में `deepcopy` और `shallowcopy` में क्या अंतर है?",
        "answer": "Shallow copy केवल आउटर ऑब्जेक्ट की नई कॉपी बनाती है (nested संदर्भ वही रहते हैं), जबकि Deep copy सभी nested ऑब्जेक्ट्स की भी पूरी तरह स्वतंत्र कॉपी बनाती है।"
    }
]

def get_daily_question():
    q = random.choice(STUDY_QUESTIONS)
    return f"📌 [{q['topic']}] {q['question']}\n💡 उत्तर: {q['answer']}"

def send_telegram_message(message):
    if TELEGRAM_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print("Telegram Bot Token सेट नहीं है।")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload, timeout=30)
        print("Telegram पर मैसेज सफलता से भेज दिया गया है!")
    except Exception as e:
        print(f"Telegram भेजने में त्रुटि: {e}")


def main():
    today_str = datetime.date.today().strftime("%A, %B %d, %Y")
    weather_info = get_weather(CITY, WEATHER_API_KEY)
    occasion_info = get_occasion(COUNTRY_CODE, HOLIDAY_API_KEY)
    study_question = get_daily_question()

    briefing = (
        f"📅 DAILY BRIEFING: {today_str}\n\n"
        f"🌤 Weather ({CITY}): {weather_info}\n"
        f"🎉 Occasion/Holiday: {occasion_info}\n\n"
        f"🧠 QUESTION OF THE DAY:\n{study_question}"
    )

    print(briefing)
    send_telegram_message(briefing)
    
if __name__ == "__main__":
    main()
