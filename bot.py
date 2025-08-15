import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token bot Telegram của bạn
TOKEN = "8204925535:AAHMVkaaBbLA3Bls5c0MFr-X8sl36PRa_co"

# Lưu túi đồ từng người chơi
inventory = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐉 Chào mừng bạn đến với game ĐÁNH QUÁI NHẬN ĐỒ!\n"
        "Dùng lệnh /hunt để đi săn quái.\n"
        "Dùng lệnh /inventory để xem túi đồ."
    )

async def hunt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    monsters = ["🐺 Sói", "🐉 Rồng", "🦂 Bọ Cạp", "👹 Yêu Quái"]
    loots = ["⚔️ Kiếm", "🛡 Khiên", "💎 Ngọc", "🍀 Bùa May Mắn", "🏹 Cung"]

    monster = random.choice(monsters)
    loot = random.choice(loots)
    win = random.choice([True, False])

    if win:
        inventory.setdefault(user_id, []).append(loot)
        await update.message.reply_text(f"{user_name} đã đánh bại {monster} và nhặt được {loot}!")
    else:
        await update.message.reply_text(f"{user_name} bị {monster} đánh bại! Không có đồ 😢")

async def show_inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    items = inventory.get(user_id, [])
    if items:
        await update.message.reply_text("🎒 Túi đồ của bạn:\n" + ", ".join(items))
    else:
        await update.message.reply_text("🎒 Túi đồ của bạn đang trống.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hunt", hunt))
    app.add_handler(CommandHandler("inventory", show_inventory))
    app.run_polling()

if __name__ == "__main__":
    main()
