import requests
import datetime

# --- CẤU HÌNH ---
TOKEN = "8424584066:AAFAYhjVsiUBLNl4UXZKEQ0zEYzTxwexsKg"
CHAT_ID = "-4669194033"
# Chọn một ngày Thứ 2 làm mốc bắt đầu chu kỳ (Ví dụ: 05/01/2026)
ANCHOR_DATE = datetime.date(2026, 2, 9) 

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def check_sprint():
    today = datetime.date.today()
    # Tính số ngày kể từ ngày gốc
    delta_days = (today - ANCHOR_DATE).days
    # Một chu kỳ 2 Sprint (20 ngày làm việc) tương đương 28 ngày lịch (4 tuần)
    current_cycle_day = delta_days % 28 
    
    # Logic xác định ngày gửi (Giả sử chu kỳ gửi nằm ở 14 ngày đầu của mốc 28 ngày)
    is_sprint_period = current_cycle_day < 14
    
    if not is_sprint_period:
        return # Không phải đợt kết thúc Sprint này, bỏ qua.

    day_of_week = today.weekday() # 0: Thứ 2, ..., 4: Thứ 6
    message = ""

    # 1. Team Debuffer: Thứ 6 đầu tiên của chu kỳ (Ngày thứ 11 tính từ Thứ 2 gốc)
    if current_cycle_day == 11: 
        message = "Chị Hương ơi cập nhật review team Debuffer"

    # 2. Team Infinity: Thứ 6 tiếp theo (Ngày thứ 25 tính từ Thứ 2 gốc)
    # Nhưng vì ta muốn 2 sprint gửi 1 lần, ta check ngày 25 trong chu kỳ 28 ngày
    elif current_cycle_day == 25:
        message = "Chị Hương ơi cập nhật review team Infinity"

    # 3. Team Skybow: Thứ 2 tiếp theo ngay sau Infinity (Ngày thứ 0 của chu kỳ mới)
    elif current_cycle_day == 0:
        message = "Chị Hương ơi cập nhật review team Skybow"

    if message:
        send_telegram(message)

if __name__ == "__main__":
    check_sprint()
