import telebot
from telebot import types

# التوكن الخاص بالبوت
TOKEN = "9294468427:AAGOHNplOfxQBdoTRSaxOb4mp0lzo_-mrOA"
ADMIN_ID = 7100695188
CHANNEL = "@valoichansy"

bot = telebot.TeleBot(TOKEN)

# إزالة أي تضارب أو جلسات معلقة قبل التشغيل
bot.remove_webhook()

# قاعدة بيانات وهمية لتخزين بيانات المستخدمين والأرصدة
users_data = {}

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
    
    # تسجيل المستخدم إذا لم يكن موجوداً
    if user_id not in users_data:
        users_data[user_id] = {'balance': 0, 'refs': 0}
        
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
    btn_ref = types.KeyboardButton("👥 دعوة أصدقاء")
    markup.add(btn_play, btn_balance)
    markup.add(btn_deposit, btn_withdraw)
    markup.add(btn_ref)
    
    bot.send_message(
        chat_id,
        "🐊 **أهلاً بك في Valo Croco Bot!**\n\n"
        "اختر ما ترغب به من القناة أدناه:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ لم تقم بالاشتراك في القناة بعد!", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    
    if not is_subscribed(user_id):
        send_welcome(message)
        return
        
    text = message.text
    
    if text == "💰 رصيدي":
        bal = users_data.get(user_id, {}).get('balance', 0)
        bot.send_message(message.chat.id, f"💳 رصيدك الحالي: **{bal} SYP**", parse_mode="Markdown")
        
    elif text == "📥 إيداع رصيد":
        bot.send_message(
            message.chat.id,
            "📥 **تعليمات الإيداع:**\n\n"
            "• الحد الأدنى للإيداع: **20,000 SYP**\n"
            "• مكسبة إيداع: **15% بونص**\n"
            "• للتحويل عبر Syriatel Cash: `21938770`\n\n"
            "بعد التحويل، أرسل صورة الإيصال للإدارة.",
            parse_mode="Markdown"
        )
        
    elif text == "📤 سحب أرباح":
        bot.send_message(
            message.chat.id,
            "📤 **تعليمات السحب:**\n\n"
            "• الحد الأدنى للسحب: **50,000 SYP**\n"
            "• التحويل يتم عبر Syriatel Cash.\n"
            "تواصل مع الإدارة لطلب السحب.",
            parse_mode="Markdown"
        )
        
    elif text == "👥 دعوة أصدقاء":
        bot.send_message(
            message.chat.id,
            "👥 **نظام الإحالات:**\n\n"
            "احصل على **3,000 SYP** عن كل صديق تدعوه!\n"
            f"رابط دعوتك: `https://t.me/{bot.get_me().username}?start={user_id}`",
            parse_mode="Markdown"
        )
        
    elif text == "🎮 العب واكسب":
        bot.send_message(message.chat.id, "🎮 قريباً جداً سيتم إطلاق ألعاب الكازينو الممتعة داخل الويب أب!")

print("Bot is running...")
bot.infinity_polling()
      
