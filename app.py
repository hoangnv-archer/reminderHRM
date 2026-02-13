import requests
import datetime
import os

# --- CẤU HÌNH ---
# Token và ID đã được làm sạch ký tự lạ
TOKEN = "8424584066:AAFAYhjVsiUBLNl4UXZKEQ0zEYzTxwexsKg"
CHAT_ID = -4669194033

# Mốc tính Sprint (Chọn Thứ 2 của tuần đầu tiên bạn muốn đếm là Sprint 1)
# Ví dụ: Ngày 05/01/2026 là bắt đầu Sprint 1 của năm
ANCHOR_DATE = datetime.date(2026, 1, 5)

def send_telegram(message):
    # Đảm bảo đường dẫn API không chứa ký tự lạ
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
        print(f"Error sending message: {e}")

def check_sprint():
    today = datetime.date.today()
    week_num = today.isocalendar()[1]
    day_of_week = today.weekday() # 0: Thứ 2, 4: Thứ 6
    cycle_pos = week_num % 4

    # Tính số thứ tự Sprint (2 tuần/Sprint)
    days_since_anchor = (today - ANCHOR_DATE).days
    sprint_num = (days_since_anchor // 14) + 1

    print(f"Today: {today} | Week: {week_num} | Cycle: {cycle_pos} | Day: {day_of_week} | Sprint: {sprint_num}")

    message = ""

    # Logic gửi tin nhắn theo yêu cầu 3 Team gối đầu
    if cycle_pos == 3 and day_of_week == 4: 
        message = f"🌌 **TEAM INFINITY**\nHôm nay là Thứ 6 - Kết thúc **Sprint {sprint_num}**!"
    
    elif cycle_pos == 0 and day_of_week == 0:
        # Skybow kết thúc Thứ 2 sau Infinity (thường là tuần mới nên dùng số Sprint cũ)
        message = f"🏹 **TEAM SKYBOW**\nHôm nay là Thứ 2 - Kết thúc **Sprint {sprint_num - 1}**!"
        
    elif cycle_pos == 2 and day_of_week == 4:
        message = f"🚀 **TEAM DEBUFFER**\nHôm nay là Thứ 6 - Kết thúc **Sprint {sprint_num}**!"

    if message:
        send_telegram(message)
    else:
        # Dòng này để test, nếu muốn ép gửi tin nhắn để kiểm tra Token hãy bỏ dấu # ở dưới
        # send_telegram("🔔 Bot đang chạy nhưng hôm nay không phải ngày kết thúc Sprint.")
        print("Không có team nào khớp lịch hôm nay.")

if __name__ == "__main__":
    check_sprint()
