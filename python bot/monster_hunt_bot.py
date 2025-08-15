#!/usr/bin/env python3
# monster_hunt_bot.py
import os
import random
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Dữ liệu tạm: players[user_id] = {...}
players = {}

# Danh sách quái + phần thưởng
monsters = [
    {"name": "Slime xanh", "hp": 5, "gold": (5, 15), "xp": (3, 7), "loot": ["Slime gel", "Mảnh vải cũ"]},
    {"name": "Goblin", "hp": 10, "gold": (10, 25), "xp": (5, 10), "loot": ["Dao rỉ", "Đá cuội"]},
    {"name": "Sói hoang", "hp": 15, "gold": (15, 30), "xp": (7, 12), "loot": ["Lông sói", "Xương thú"]},
    {"name": "Orc", "hp": 20, "gold": (20, 40), "xp": (10, 15), "loot": ["Rìu gãy", "Da thú"]}
]

# Tính XP cần để lên level
def xp_to_next(level):
    return 20 + (level - 1) * 10

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        players[user_id] = {
            "name": update.effective_user.first_name,
            "level": 1,
            "xp": 0,
            "gold": 0,
            "inventory": []
        }
        await update.message.reply_text(f"🎮 Xin chào {update.effective_user.first_name}! Nhân vật của bạn đã được tạo.\nGõ /hunt để đi săn quái.")
    else:
        await update.message.reply_text("Bạn đã có nhân vật rồi! Gõ /hunt để đi săn.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        await update.message.reply_text("Bạn chưa có nhân vật. Gõ /start để bắt đầu.")
        return
    p = players[user_id]
    xp_needed = xp_to_next(p["level"])
    await update.message.reply_text(
        f"📜 Thông tin nhân vật:\n"
        f"👤 Tên: {p['name']}\n"
        f"🏅 Level: {p['level']}\n"
        f"⭐ XP: {p['xp']}/{xp_needed}\n"
        f"💰 Gold: {p['gold']}\n"
        f"🎒 Số đồ: {len(p['inventory'])}"
    )

async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        await update.message.reply_text("Bạn chưa có nhân vật. Gõ /start để bắt đầu.")
        return
    inv = players[user_id]["inventory"]
    if not inv:
        await update.message.reply_text("🎒 Túi đồ của bạn trống rỗng.")
    else:
        items = "\n".join(f"- {i}" for i in inv)
        await update.message.reply_text(f"🎒 Túi đồ:\n{items}")

async def hunt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        await update.message.reply_text("Bạn chưa có nhân vật. Gõ /start để bắt đầu.")
        return
    
    monster = random.choice(monsters)
    p = players[user_id]

    # Giả lập chiến đấu thắng luôn
    gold = random.randint(*monster["gold"])
    xp = random.randint(*monster["xp"])
    loot = random.choice(monster["loot"]) if random.random() < 0.7 else None  # 70% rơi đồ

    p["gold"] += gold
    p["xp"] += xp
    if loot:
        p["inventory"].append(loot)

    msg = f"⚔️ Bạn gặp {monster['name']} và đã đánh bại nó!\n"
    msg += f"💰 Nhận {gold} gold\n"
    msg += f"⭐ Nhận {xp} XP\n"
    if loot:
        msg += f"🎁 Nhặt được: {loot}\n"

    # Kiểm tra lên level
    while p["xp"] >= xp_to_next(p["level"]):
        p["xp"] -= xp_to_next(p["level"])
        p["level"] += 1
        msg += f"🏆 Lên cấp {p['level']}!\n"

    await update.message.reply_text(msg)

def main():
    token = os.environ.get("TG_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
    if token == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        raise ValueError("❌ Chưa cấu hình token. Set TG_BOT_TOKEN env hoặc sửa code.")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("inventory", inventory))
    app.add_handler(CommandHandler("hunt", hunt))

    app.run_polling()

if __name__ == "__main__":
    main()
