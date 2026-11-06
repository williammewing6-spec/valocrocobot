import telebot
from telebot import types

# التوكن الخاص بالبوت ومعرف الآدمن
TOKEN = "9294468427:AAGOHNplOfxQBdoTRSaxOb4mp0lzo_-mrOA"
ADMIN_ID = 7100695188
CHANNEL = "@valoichansy"

bot = telebot.TeleBot(TOKEN)

# إزالة أي جلسات معلقة لمنع مشكلة الكونفليكت
bot.remove_webhook()

# قاعدة بيانات لتخزين المستخدمين (الأرصدة، الإحالات، وحالات الإدخال المؤقتة)
users_data = {}
user_state = {}

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except:
        pass
    return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # معالجة نظام الإحالات إذا تم استخدام رابط دعوة
    args = message.text.split()
    if len(args) > 1:
        try:
            referrer_id = int(args[1])
            if referrer_id != user_id and referrer_id in users_data:
                if user_id not in users_data:
                    # مستخدم جديد تم دعوته
                    if 'referred_by' not in users_data.get(user_id, {}):
                        users_data.setdefault(referrer_id, {'balance': 0, 'refs': 0, 'ref_list': []})
                        if user_id not in users_data[referrer_id]['ref_list']:
                            users_data[referrer_id]['refs'] += 1
                            users_data[referrer_id]['ref_list'].append(user_id)
                            # مكافأة الإحالة 3000 ليرة مثلاً
                            users_data[referrer_id]['balance'] += 3000
                            bot.send_message(referrer_id, f"🎉 انضم صديق جديد عبر رابط إحالتك! تم إضافة 3,000 SYP لرصيدك.")
        except:
            pass

    # تسجيل المستخدم إذا لم يكن موجوداً
    if user_id not in users_data:
        users_data[user_id] = {'balance': 0, 'refs': 0, 'ref_list': []}
        
    # فحص الاشتراك الإجباري
    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        btn_channel = types.InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL.replace('@', '')}")
        btn_check = types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub")
        markup.add(btn_channel)
        markup.add(btn_check)
        
        bot.send_message(
            message.chat.id,
            "⚠️ **عليك الاشتراك في قناة البوت أولاً لتتمكن من استخدامه!**\n\n"
            f"القناة: {CHANNEL}\n"
            "بعد الاشتراك، اضغط على زر (تحقق من الاشتراك) 👇",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_play = types.KeyboardButton("🎮 العب واكسب")
    btn_balance = types.KeyboardButton("💰 رصيدي")
    btn_deposit = types.KeyboardButton("📥 إيداع رصيد")
    btn_withdraw = types.KeyboardButton("📤 سحب أرباح")
    btn_ref = types.KeyboardButton("👥 الإحالات")
    btn_support = types.KeyboardButton("🛠️ تواصل مع الدعم")
    markup.add(btn_play, btn_balance)
    markup.add(btn_deposit, btn_withdraw)
    markup.add(btn_ref, btn_support)
    
    bot.send_message(
        chat_id,
        "🐊 **أهلاً بك في Valo Croco Bot!**\n\n"
        "اختر ما ترغب به من القائمة أدناه:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check(
          
