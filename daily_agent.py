import datetime
import os
import random
import requests
from twilio.rest import Client

# --- 1. कॉन्फ़िगरेशन (Configurations) ---
CITY = "Delhi"
COUNTRY_CODE = "IN"

# Weather & Holiday API Keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "8zb140d8859e21c72d5d5956ecd2175")
HOLIDAY_API_KEY = os.getenv("HOLIDAY_API_KEY", "EtGpkue87chwT7BPmPTUffxr5yqBfUrp")

# Telegram Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8706649605:AAFOdAerAWQ7E3vuB9gM93tq7-fpS5qFBRc")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "6125641152")

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "AC7e2b6ae0e747fba2f1665443e7823c94")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "42709aaab8f68e144540768003cc324a")
FROM_WHATSAPP = os.getenv("FROM_WHATSAPP", "whatsapp:+14155238886")  # Twilio Sandbox Number
TO_WHATSAPP = os.getenv("TO_WHATSAPP", "whatsapp:+919569092645")      # Your WhatsApp Number

# --- 2. Study Question Bank ---
STUDY_QUESTIONS = [
    {
        "topic": "SQL",
        "question": "WHERE और HAVING clause में क्या अंतर है?",
        "answer": "WHERE aggregates से पहले rows फ़िल्टर करता है, जबकि HAVING क्लॉज़ GROUP BY के बाद aggregate रिजल्ट्स फ़िल्टर करता है।"
    },
    {
        "topic": "Python",
        "question": "Python में list और tuple के बीच मुख्य अंतर क्या है?",
        "answer": "List Mutable होती है [], जबकि Tuple Immutable होता है ()।"
    },
    {
        "topic": "SQL",
        "question": "PRIMARY KEY और UNIQUE KEY में क्या अंतर है?",
        "answer": "Primary Key में NULL मान नहीं हो सकता, जबकि Unique Key एक NULL मान की अनुमति देती है।"
    },
    {
        "topic": "Data Analytics",
        "question": "Data Analytics में Mean, Median और Mode क्या हैं?",
        "answer": "Mean औसत है, Median मध्य मान है, और Mode सबसे अधिक बार आने वाला मान है।"
    },
    {
        "topic": "Python",
        "question": "Python में deepcopy और shallowcopy में क्या अंतर है?",
        "answer": "Shallow copy आउटर ऑब्जेक्ट कॉपी करती है, जबकि Deep copy सभी nested ऑब्जेक्ट्स की स्वतंत्र कॉपी बनाती है।"
    }
]

# --- 3. Helper Functions ---
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            return f"{temp}°C, {desc}"
        return "मौसम डेटा उपलब्ध नहीं है"
    except Exception as e:
        return f"मौसम नेटवर्क एरर: {e}"

def get_occasion(country, api_key):
    today = datetime.date.today()
    url = f"https://calendarific.com/api/v2/holidays?api_key={api_key}&country={country}&year={today.year}&day={today.day}&month={today.month}"
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        holidays = data.get("response", {}).get("holidays", [])
        if holidays:
            names = [h["name"] for h in holidays]
            return ", ".join(names)
        return "आज कोई मुख्य सार्वजनिक अवकाश नहीं है"
    except Exception as e:
        return f"त्यौहार नेटवर्क एरर: {e}"

def get_daily_question():
    q = random.choice(STUDY_QUESTIONS)
    return f"📌 [{q['topic']}] {q['question']}\n💡 उत्तर: {q['answer']}"

# --- 4. Messaging Functions ---
def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram Config missing. Skipping Telegram notification.")
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            print("✅ Telegram पर मैसेज सफलता से भेज दिया गया है!")
        else:
            print(f"❌ Telegram Error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram भेजने में त्रुटि: {e}")

def send_whatsapp_message(message):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print("⚠️ Twilio Credentials missing. Skipping WhatsApp notification.")
        return

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP
        )
        print(f"✅ WhatsApp मैसेज सफलता से भेजा गया! SID: {msg.sid}")
    except Exception as e:
        print(f"❌ WhatsApp भेजने में त्रुटि: {e}")

# --- 5. Main Execution ---
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

    print("--- GENERATED BRIEFING ---")
    print(briefing)
    print("--------------------------")
    
    # Send to active channels
    send_telegram_message(briefing)
    send_whatsapp_message(briefing)

if __name__ == "__main__":
    main()
