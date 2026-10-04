import telebot
from telebot import types
import json
import os
from datetime import datetime

# ====================== НАСТРОЙКИ ======================
TOKEN = os.getenv("BOT_TOKEN") or "ВСТАВЬ_ТОКЕН_СЮДА"
ADMIN_IDS = [123456789]  # <-- ЗАМЕНИ НА СВОЙ TELEGRAM ID

bot = telebot.TeleBot(TOKEN)

# ====================== ДАННЫЕ ======================
JOBS = [
    {"id": 1, "name": "Курьер", "level": 1, "pay": 180, "energy": 15, "mood": -5},
    {"id": 2, "name": "Промоутер", "level": 1, "pay": 150, "energy": 12, "mood": -8},
    {"id": 3, "name": "Грузчик", "level": 1, "pay": 220, "energy": 25, "mood": -10},
    {"id": 4, "name": "Официант", "level": 2, "pay": 280, "energy": 18, "mood": -6},
    {"id": 5, "name": "Кассир", "level": 2, "pay": 250, "energy": 14, "mood": -7},
    {"id": 6, "name": "Таксист", "level": 3, "pay": 420, "energy": 20, "mood": -5},
    {"id": 7, "name": "Бармен", "level": 3, "pay": 380, "energy": 16, "mood": 2},
    {"id": 8, "name": "Менеджер магазина", "level": 4, "pay": 550, "energy": 18, "mood": -3},
    {"id": 9, "name": "SMM-специалист", "level": 4, "pay": 600, "energy": 12, "mood": 5},
    {"id": 10, "name": "Продавец", "level": 3, "pay": 320, "energy": 15, "mood": -4},
    {"id": 11, "name": "Программист-джун", "level": 5, "pay": 900, "energy": 20, "mood": 3},
    {"id": 12, "name": "Маркетолог", "level": 5, "pay": 850, "energy": 15, "mood": 4},
    {"id": 13, "name": "Дизайнер", "level": 5, "pay": 780, "energy": 14, "mood": 8},
    {"id": 14, "name": "Риелтор", "level": 6, "pay": 1100, "energy": 18, "mood": 2},
    {"id": 15, "name": "Бухгалтер", "level": 5, "pay": 720, "energy": 16, "mood": -2},
    {"id": 16, "name": "Тимлид", "level": 7, "pay": 1600, "energy": 22, "mood": 5},
    {"id": 17, "name": "Продуктовый менеджер", "level": 8, "pay": 2100, "energy": 20, "mood": 6},
    {"id": 18, "name": "Юрист", "level": 7, "pay": 1800, "energy": 18, "mood": 3},
    {"id": 19, "name": "Врач", "level": 8, "pay": 2400, "energy": 25, "mood": 4},
    {"id": 20, "name": "Директор филиала", "level": 9, "pay": 3200, "energy": 24, "mood": 7},
    {"id": 21, "name": "CTO", "level": 10, "pay": 5500, "energy": 28, "mood": 8},
    {"id": 22, "name": "Генеральный директор", "level": 12, "pay": 9000, "energy": 30, "mood": 10},
]

BUSINESSES = [
    {"id": 1, "name": "Ларьёк с шаурмой", "price": 2500, "income": 180, "level": 1},
    {"id": 2, "name": "Кофейня", "price": 8000, "income": 450, "level": 2},
    {"id": 3, "name": "Автомойка", "price": 15000, "income": 700, "level": 3},
    {"id": 4, "name": "Магазин у дома", "price": 22000, "income": 950, "level": 3},
    {"id": 5, "name": "Барбершоп", "price": 18000, "income": 820, "level": 3},
    {"id": 6, "name": "Фитнес-студия", "price": 35000, "income": 1400, "level": 4},
    {"id": 7, "name": "Автосервис", "price": 45000, "income": 1800, "level": 5},
    {"id": 8, "name": "Ресторан", "price": 80000, "income": 2800, "level": 6},
    {"id": 9, "name": "Сеть кофеен", "price": 120000, "income": 4200, "level": 7},
    {"id": 10, "name": "IT-компания", "price": 200000, "income": 6500, "level": 8},
    {"id": 11, "name": "Логистика", "price": 350000, "income": 9800, "level": 9},
    {"id": 12, "name": "Сеть магазинов", "price": 500000, "income": 14000, "level": 10},
    {"id": 13, "name": "Завод", "price": 1200000, "income": 28000, "level": 12},
    {"id": 14, "name": "Холдинг", "price": 5000000, "income": 95000, "level": 15},
]

# ====================== ХРАНИЛИЩЕ ======================
DATA_FILE = "players.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_player(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {
            "money": 500,
            "energy": 80,
            "mood": 70,
            "level": 1,
            "exp": 0,
            "businesses": [],
            "name": "Игрок"
        }
        save_data(data)
    return data[uid]

def update_player(user_id, player):
    data = load_data()
    data[str(user_id)] = player
    save_data(data)

# ====================== КЛАВИАТУРЫ ======================
def main_keyboard(is_admin=False):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("👤 Профиль", "💼 Работы")
    kb.row("🏢 Бизнесы", "😴 Отдохнуть")
    kb.row("💰 Собрать доход")
    if is_admin:
        kb.row("🛠 Админ")
    return kb

def jobs_keyboard(player):
    kb = types.InlineKeyboardMarkup()
    for job in JOBS:
        if player["level"] >= job["level"]:
            kb.add(types.InlineKeyboardButton(
                f"{job['name']} (+${job['pay']})",
                callback_data=f"job_{job['id']}"
            ))
    return kb

def business_keyboard(player):
    kb = types.InlineKeyboardMarkup()
    for biz in BUSINESSES:
        owned = biz["id"] in player["businesses"]
        if owned:
            text = f"✅ {biz['name']} (доход ${biz['income']})"
        else:
            text = f"{biz['name']} — ${biz['price']}"
        kb.add(types.InlineKeyboardButton(text, callback_data=f"biz_{biz['id']}"))
    return kb

# ====================== КОМАНДЫ ======================
@bot.message_handler(commands=["start"])
def start(message):
    player = get_player(message.from_user.id)
    player["name"] = message.from_user.first_name or "Игрок"
    update_player(message.from_user.id, player)
    
    is_admin = message.from_user.id in ADMIN_IDS
    bot.send_message(
        message.chat.id,
        f"Привет, {player['name']}!\n\n"
        f"Это симулятор жизни.\n"
        f"Работай, покупай бизнесы, развивайся.\n\n"
        f"Деньги: ${player['money']}\n"
        f"Уровень: {player['level']}",
        reply_markup=main_keyboard(is_admin)
    )

@bot.message_handler(func=lambda m: m.text == "👤 Профиль")
def profile(message):
    p = get_player(message.from_user.id)
    owned = []
    for bid in p["businesses"]:
        b = next((x for x in BUSINESSES if x["id"] == bid), None)
        if b:
            owned.append(f"• {b['name']} (${b['income']})")
    
    text = (
        f"👤 <b>{p['name']}</b>\n\n"
        f"💰 Деньги: <b>${p['money']:,}</b>\n"
        f"⚡ Энергия: {p['energy']}/100\n"
        f"😊 Настроение: {p['mood']}/100\n"
        f"⭐ Уровень: {p['level']} (опыт {p['exp']})\n\n"
        f"🏢 Бизнесы:\n" + ("\n".join(owned) if owned else "Пока нет")
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "💼 Работы")
def jobs(message):
    p = get_player(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"Выбери работу (твоя энергия: {p['energy']}):",
        reply_markup=jobs_keyboard(p)
    )

@bot.message_handler(func=lambda m: m.text == "🏢 Бизнесы")
def businesses(message):
    p = get_player(message.from_user.id)
    bot.send_message(
        message.chat.id,
        "Доступные бизнесы:",
        reply_markup=business_keyboard(p)
    )

@bot.message_handler(func=lambda m: m.text == "😴 Отдохнуть")
def rest(message):
    p = get_player(message.from_user.id)
    if p["energy"] >= 100:
        bot.reply_to(message, "Энергия уже полная!")
        return
    p["energy"] = min(100, p["energy"] + 25)
    p["mood"] = min(100, p["mood"] + 5)
    update_player(message.from_user.id, p)
    bot.reply_to(message, f"Ты отдохнул.\nЭнергия: {p['energy']}/100\nНастроение: {p['mood']}/100")

@bot.message_handler(func=lambda m: m.text == "💰 Собрать доход")
def collect(message):
    p = get_player(message.from_user.id)
    if not p["businesses"]:
        bot.reply_to(message, "У тебя пока нет бизнесов.")
        return
    total = 0
    for bid in p["businesses"]:
        b = next((x for x in BUSINESSES if x["id"] == bid), None)
        if b:
            total += b["income"]
    p["money"] += total
    update_player(message.from_user.id, p)
    bot.reply_to(message, f"Собрано ${total:,}!\nТеперь у тебя ${p['money']:,}")

@bot.message_handler(func=lambda m: m.text == "🛠 Админ")
def admin_panel(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("+10 000$", "+100 000$")
    kb.row("Полная энергия", "Полное настроение")
    kb.row("Сброс прогресса", "◀️ Назад")
    bot.send_message(message.chat.id, "Админ-панель:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text in ["+10 000$", "+100 000$", "Полная энергия", "Полное настроение", "Сброс прогресса", "◀️ Назад"])
def admin_actions(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    p = get_player(message.from_user.id)
    
    if message.text == "+10 000$":
        p["money"] += 10000
        bot.reply_to(message, f"+10 000$. Теперь ${p['money']:,}")
    elif message.text == "+100 000$":
        p["money"] += 100000
        bot.reply_to(message, f"+100 000$. Теперь ${p['money']:,}")
    elif message.text == "Полная энергия":
        p["energy"] = 100
        bot.reply_to(message, "Энергия восстановлена")
    elif message.text == "Полное настроение":
        p["mood"] = 100
        bot.reply_to(message, "Настроение полное")
    elif message.text == "Сброс прогресса":
        p = {"money": 500, "energy": 80, "mood": 70, "level": 1, "exp": 0, "businesses": [], "name": p.get("name", "Игрок")}
        bot.reply_to(message, "Прогресс сброшен")
    elif message.text == "◀️ Назад":
        bot.send_message(message.chat.id, "Главное меню", reply_markup=main_keyboard(True))
        return
    
    update_player(message.from_user.id, p)

# ====================== CALLBACK ======================
@bot.callback_query_handler(func=lambda call: call.data.startswith("job_"))
def do_job(call):
    job_id = int(call.data.split("_")[1])
    job = next((j for j in JOBS if j["id"] == job_id), None)
    if not job:
        return
    
    p = get_player(call.from_user.id)
    
    if p["level"] < job["level"]:
        bot.answer_callback_query(call.id, "Нужен выше уровень", show_alert=True)
        return
    if p["energy"] < job["energy"]:
        bot.answer_callback_query(call.id, "Не хватает энергии", show_alert=True)
        return
    
    p["energy"] -= job["energy"]
    p["money"] += job["pay"]
    p["mood"] = max(0, min(100, p["mood"] + job["mood"]))
    p["exp"] += job["pay"] // 10
    
    # Level up
    need = p["level"] * 100
    if p["exp"] >= need:
        p["exp"] -= need
        p["level"] += 1
        bot.send_message(call.message.chat.id, f"🎉 Уровень повышен! Теперь {p['level']}")
    
    update_player(call.from_user.id, p)
    bot.answer_callback_query(call.id, f"+${job['pay']}")
    bot.edit_message_text(
        f"Ты поработал: {job['name']}\n+${job['pay']}\nЭнергия: {p['energy']}/100",
        call.message.chat.id,
        call.message.message_id
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("biz_"))
def buy_business(call):
    biz_id = int(call.data.split("_")[1])
    biz = next((b for b in BUSINESSES if b["id"] == biz_id), None)
    if not biz:
        return
    
    p = get_player(call.from_user.id)
    
    if biz_id in p["businesses"]:
        bot.answer_callback_query(call.id, "Уже куплено", show_alert=True)
        return
    if p["money"] < biz["price"]:
        bot.answer_callback_query(call.id, "Не хватает денег", show_alert=True)
        return
    if p["level"] < biz["level"]:
        bot.answer_callback_query(call.id, "Нужен выше уровень", show_alert=True)
        return
    
    p["money"] -= biz["price"]
    p["businesses"].append(biz_id)
    update_player(call.from_user.id, p)
    
    bot.answer_callback_query(call.id, f"Куплено: {biz['name']}")
    bot.send_message(call.message.chat.id, f"✅ Ты купил «{biz['name']}»!\nДоход: ${biz['income']} за сбор")

# ====================== ЗАПУСК ======================
print("Бот запущен...")
bot.infinity_polling()
