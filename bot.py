import os
import telebot
from telebot import types
from flask import Flask

TOKEN = "9294468427:AAGOHNplOfxQBdoTRSaxOb4mp0lzo_-mrOA"
ADMIN_ID = 7100695188
CHANNELS = ["@valoichansy"]

bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()

users_data = {}
user_state = {}

# سيرفر ويب خفيف ومجاني لتلبية متطلبات Web Service على Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Valo Croco Bot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def check_all_subscriptions(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return channel
        except:
            return channel
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    args = message.text.split()
    if len(args) > 1:
        try:
            referrer_id = int(args[1])
            if referrer_id != user_id and referrer_id in users_data:
                if user_id not in users_data:
                    if 'referred_by' not in users_data.get(user_id, {}):
                        users_data.setdefault(referrer_id, {'balance': 0, 'refs': 0, 'ref_list': []})
                        if user_id not in users_data[referrer_id]['ref_list']:
                            users_data[referrer_id]['refs'] += 1
                            users_data[referrer_id]['ref_list'].append(user_id)
                            users_data[referrer_id]['balance'] += 3000
                            bot.send_message(referrer_id, f"🎉 انضم صديق جديد عبر رابط إحالتك! تم إضافة 3,000 SYP لرصيدك.")
        except:
            pass

    if user_id not in users_data:
        users_data[user_id] = {'balance': 0, 'refs': 0, 'ref_list': []}
        
    unsubscribed_channel = check_all_subscriptions(user_id)
    if unsubscribed_channel:
        markup = types.InlineKeyboardMarkup()
        for ch in CHANNELS:
            ch_clean = ch.replace('@', '')
            markup.add(types.InlineKeyboardButton(f"📢 اشترك في {ch}", url=f"https://t.me/{ch_clean}"))
        markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub"))
        
        bot.send_message(
            message.chat.id,
            "⚠️ **عليك الاشتراك في قناة البوت أولاً لتتمكن من استخدامه!**\n\n"
            "اشترك في القناة ثم اضغط (تحقق من الاشتراك) 👇",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    show_main_menu(message.chat.id)

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ هذا الأمر مخصص للإدارة فقط.")
        return
        
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📊 إحصائيات البوت", callback_data="admin_stats"))
    markup.add(types.InlineKeyboardButton("📢 إرسال إشعار للكل", callback_data="admin_broadcast"))
    
    bot.send_message(
        message.chat.id,
        "👑 **أهلاً بك في لوحة تحكم الآدمن الخاصة بـ Valo Croco Bot**\n\n"
        "جميع طلبات الإيداع، السحب، والدعم الفني ستصلك هنا مباشرة كرسائل تنبيه.",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data in ["admin_stats", "admin_broadcast"])
def admin_callbacks(call):
    if call.from_user.id != ADMIN_ID:
        return
    if call.data == "admin_stats":
        total_users = len(users_data)
        bot.answer_callback_query(call.id, f"عدد المستخدمين المسجلين: {total_users}", show_alert=True)
    elif call.data == "admin_broadcast":
        bot.answer_callback_query(call.id, "ميزة الإذاعة قيد التطوير", show_alert=True)

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
def callback_check(call):
    user_id = call.from_user.id
    if check_all_subscriptions(user_id) is None:
        bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ لم تقم بالاشتراك في القناة بعد!", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    text = message.text
    
    if user_id in user_state:
        state = user_state[user_id]
        
        if state == 'withdraw_syriatel_phone':
            user_state[user_id] = {'step': 'withdraw_syriatel_amount', 'phone': text}
            bot.send_message(message.chat.id, "📱 أرسل الآن **المبلغ المطلوب سحبه**:", parse_mode="Markdown")
            return
            
        elif isinstance(state, dict) and state.get('step') == 'withdraw_syriatel_amount':
            phone = state.get('phone')
            amount = text
            user_state.pop(user_id, None)
            
            bot.send_message(message.chat.id, "✅ تم إرسال طلب السحب للإدارة بنجاح وسيتم معالجته قريباً.")
            bot.send_message(
                ADMIN_ID,
                f"📤 **طلب سحب جديد (Syriatel Cash):**\n\n"
                f"👤 المستخدم: `{user_id}`\n"
                f"📱 الرقم: `{phone}`\n"
                f"💰 المبلغ: `{amount}`",
                parse_mode="Markdown"
            )
            return

        elif state == 'withdraw_cham_code':
            user_state[user_id] = {'step': 'withdraw_cham_amount', 'code': text}
            bot.send_message(message.chat.id, "💬 أرسل الآن **المبلغ المطلوب سحبه**:", parse_mode="Markdown")
            return
            
        elif isinstance(state, dict) and state.get('step') == 'withdraw_cham_amount':
            code = state.get('code')
            amount = text
            user_state.pop(user_id, None)
            
            bot.send_message(message.chat.id, "✅ تم إرسال طلب السحب للإدارة بنجاح وسيتم معالجته قريباً.")
            bot.send_message(
                ADMIN_ID,
                f"📤 **طلب سحب جديد (Cham Cash):**\n\n"
                f"👤 المستخدم: `{user_id}`\n"
                f"🔑 الكود: `{code}`\n"
                f"💰 المبلغ: `{amount}`",
                parse_mode="Markdown"
            )
            return

        elif state == 'support_message':
            user_state.pop(user_id, None)
            bot.send_message(message.chat.id, "✅ تم إرسال مشكلتك إلى الدعم الفني بنجاح، سيتم الرد عليك قريباً.")
            bot.send_message(
                ADMIN_ID,
                f"🛠️ **رسالة دعم فني جديدة:**\n\n"
                f"👤 من المستخدم: `{user_id}`\n"
                f"📝 الرسالة:\n{text}\n\n"
                f"*(للرد على المستخدم قم بنسخ الآيدي والرد عليه مباشرة)*",
                parse_mode="Markdown"
            )
            return

    if check_all_subscriptions(user_id) is not None:
        send_welcome(message)
        return
        
    if text == "💰 رصيدي":
        bal = users_data.get(user_id, {}).get('balance', 0)
        bot.send_message(message.chat.id, f"💳 رصيدك الحالي: **{bal} SYP**", parse_mode="Markdown")
        
    elif text == "📥 إيداع رصيد":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("سيرياتيل كاش (15%)", callback_data="dep_syriatel"))
        markup.add(types.InlineKeyboardButton("شام كاش (25%)", callback_data="dep_cham"))
        bot.send_message(
            message.chat.id,
            "📥 **اختر طريقة الإيداع المناسبة:**",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        
    elif text == "📤 سحب أرباح":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("سيرياتيل كاش", callback_data="with_syriatel"))
        markup.add(types.InlineKeyboardButton("شام كاش", callback_data="with_cham"))
        bot.send_message(
            message.chat.id,
            "📤 **اختر طريقة السحب المناسبة:**",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        
    elif text == "👥 الإحالات":
        user_info = users_data.get(user_id, {'balance': 0, 'refs': 0})
        refs_count = user_info.get('refs', 0)
        bot.send_message(
            message.chat.id,
            "👥 **نظام الإحالات والأرباح:**\n\n"
            f"📊 عدد أصدقائك المدعوين (الإحالات): **{refs_count}** شخص\n"
            "احصل على مكافأة عن كل صديق تدعوه!\n\n"
            f"🔗 رابط دعوتك الشخصي:\n`https://t.me/{bot.get_me().username}?start={user_id}`",
            parse_mode="Markdown"
        )
        
    elif text == "🛠️ تواصل مع الدعم":
        user_state[user_id] = 'support_message'
        bot.send_message(message.chat.id, "🛠️ أرسل رسالتك أو مشكلتك الآن، وسيتم تحويلها مباشرة إلى الإدارة:")
        
    elif text == "🎮 العب واكسب":
        bot.send_message(message.chat.id, "🎮 قريباً جداً سيتم إطلاق ألعاب الكازينو الممتعة داخل البوت!")

@bot.callback_query_handler(func=lambda call: call.data in ["dep_syriatel", "dep_cham", "with_syriatel", "with_cham"])
def callback_deposits_withdrawals(call):
    user_id = call.from_user.id
    data = call.data
    
    if data == "dep_syriatel":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "📥 **إيداع عبر سيرياتيل كاش (15% بونص):**\n\n"
            "• للتحويل عبر الرقم: `21938770`\n"
            "بعد التحويل، أرسل صورة الإيصال أو تفاصيل التحويل للإدارة.",
            parse_mode="Markdown"
        )
    elif data == "dep_cham":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "📥 **إيداع عبر شام كاش (25% بونص):**\n\n"
            "• كود الحساب / المحفظة الخاص بالشام كاش: `CHAM_CODE_12345`\n"
            "بعد التحويل، أرسل صورة الإيصال أو تفاصيل التحويل للإدارة.",
            parse_mode="Markdown"
        )
    elif data == "with_syriatel":
        bot.answer_callback_query(call.id)
        user_state[user_id] = 'withdraw_syriatel_phone'
        bot.send_message(call.message.chat.id, "📱 أرسل **رقم سيرياتيل كاش** الذي تريد السحب عليه:")
    elif data == "with_cham":
        bot.answer_callback_query(call.id)
        user_state[user_id] = 'withdraw_cham_code'
        bot.send_message(call.message.chat.id, "🔑 أرسل **كود حساب شام كاش** الذي تريد السحب عليه:")

if __name__ == "__main__":
    import threading
    t = threading.Thread(target=run_web)
    t.start()
    print("Bot and Web Server are running...")
    bot.infinity_polling()
