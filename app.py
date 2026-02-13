import requests
import datetime
import os
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
# Chọn một ngày Thứ 2 làm mốc bắt đầu chu kỳ (Ví dụ: 05/01/2026)
ANCHOR_DATE = datetime.date(2026, 2, 9) 

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    print(f"Telegram Response: {response.status_code} - {response.text}")

def check_sprint():
    today = datetime.date.today()
    week_num = today.isocalendar()[1]
    day_of_week = today.weekday() # 0: Thứ 2, 4: Thứ 6
    cycle_pos = week_num % 4

    print(f"Today: {today} | Week Num: {week_num} | Cycle Pos: {cycle_pos} | Day: {day_of_week}")

    message = ""

    # ĐIỀU CHỈNH LOGIC TẠI ĐÂY:
    # Nếu hôm nay (Thứ 6 ngày 13/02) là ngày của Team Infinity:
    if cycle_pos == 3 and day_of_week == 4: 
        message = "🌌 **TEAM INFINITY**\nHôm nay là Thứ 6 - Kết thúc Sprint!"
    
    # Team Skybow sẽ là Thứ 2 tuần tới (Tuần 8 -> 8%4 = 0)
    elif cycle_pos == 0 and day_of_week == 0:
        message = "🏹 **TEAM SKYBOW**\nHôm nay là Thứ 2 - Kết thúc Sprint!"
        
    # Team Debuffer sẽ là Thứ 6 tuần tới nữa (Tuần 9 -> 9%4 = 1)
    elif cycle_pos == 2 and day_of_week == 4:
        message = "🚀 **TEAM DEBUFFER**\nHôm nay là Thứ 6 - Kết thúc Sprint!"

    if message:
        print(f"Sending: {message}")
        send_telegram(message)
    else:
        print("Không có team nào khớp lịch hôm nay. Bot sẽ không gửi tin nhắn.")

if __name__ == "__main__":
    check_sprint()
