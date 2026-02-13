import requests
import datetime
import os

# --- CẤU HÌNH CHUNG ---
TOKEN = "8424584066:AAFAYhjVsiUBLNl4UXZKEQ0zEYzTxwexsKg"
CHAT_ID = -4669194033

# --- CẤU HÌNH RIÊNG TỪNG TEAM ---
# Bạn có thể chỉnh ngày bắt đầu và số Sprint hiện tại ở đây
TEAMS_CONFIG = {
    "DEBUFFER": {
        "start_date": datetime.date(2026, 1, 2), # Ngày Thứ 6 của Sprint X nào đó
        "start_sprint_num": 6                   # Số Sprint tại ngày đó
    },
    "INFINITY": {
        "start_date": datetime.date(2026, 1, 16),
        "start_sprint_num": 32
    },
    "SKYBOW": {
        "start_date": datetime.date(2026, 1, 19), # Ngày Thứ 2
        "start_sprint_num": 12
    }
}

def calculate_sprint_num(team_name, today):
    config = TEAMS_CONFIG[team_name]
    # Tính số ngày chênh lệch kể từ ngày mốc
    delta_days = (today - config["start_date"]).days
    # Cứ mỗi 14 ngày (2 tuần) là tăng 1 Sprint
    sprint_offset = delta_days // 14
    return config["start_sprint_num"] + sprint_offset

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN.strip()}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Telegram Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def check_sprint():
    today = datetime.date.today()
    week_num = today.isocalendar()[1]
    day_of_week = today.weekday() # 0: Thứ 2, 4: Thứ 6
    cycle_pos = week_num % 4

    print(f"Today: {today} | Cycle: {cycle_pos} | Day: {day_of_week}")

    message = ""

    # 1. Team Infinity: Thứ 6 (Tuần 3 chu kỳ)
    if cycle_pos == 3 and day_of_week == 4:
        s_num = calculate_sprint_num("INFINITY", today)
        message = f"🌌 **TEAM INFINITY**\nHôm nay là Thứ 6 - Kết thúc **Sprint {s_num}\nCập nhật review đê!!!!!!**"

    # 2. Team Skybow: Thứ 2 (Tuần 0 chu kỳ)
    elif cycle_pos == 0 and day_of_week == 0:
        s_num = calculate_sprint_num("SKYBOW", today)
        message = f"🏹 **TEAM SKYBOW**\nHôm nay là Thứ 2 - Kết thúc **Sprint {s_num}\nCập nhật review đê!!!!!!**"

    # 3. Team Debuffer: Thứ 6 (Tuần 2 chu kỳ)
    elif cycle_pos == 2 and day_of_week == 4:
        s_num = calculate_sprint_num("DEBUFFER", today)
        message = f"🚀 **TEAM DEBUFFER**\nHôm nay là Thứ 6 - Kết thúc **Sprint {s_num}\nCập nhật review đê!!!!!!**"

    if message:
        send_telegram(message)
    else:
        print("Không có team nào khớp lịch hôm nay.")

if __name__ == "__main__":
    check_sprint()
