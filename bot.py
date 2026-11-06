import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "9294468427:AAGOHNplOfxQBdoTRSaxOb4mp0lzo_-mrOA"
ADMIN_ID = 7100695188  # آيدي الآدمن الخاص بك
CHANNEL_USERNAME = "@valoichansy"  # قناة الاشتراك الإجباري

bot = telebot.TeleBot(TOKEN)

# دالة للتحقق من الاشتراك الإجباري
def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'creator', 'administrator']:
            return True
    except:
        pass
    return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # فحص الاشتراك الإجباري
    if not check_sub(user_id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 اشترك في القناة هنا", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"))
        markup.add(InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription"))
        bot.send_message(
            message.chat.id, 
            "⚠️ **عذراً، يجب عليك الاشتراك في قناة البوت أولاً لاستخدامه!**\n\nاشترك بالقناة ثم اضغط على زر التحقق.", 
            parse_mode="Markdown", 
            reply_markup=markup
        )
        return

    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    
    btn_play = InlineKeyboardButton("🎮 ألعاب الكازينو", web_app=telebot.types.WebAppInfo(url="https://google.com"))
    btn_deposit = InlineKeyboardButton("💰 شحن رصيد (20 ألف)", callback_data="deposit_menu")
    btn_withdraw = InlineKeyboardButton("💳 سحب أرباح", callback_data="withdraw_menu")
    btn_account = InlineKeyboardButton("👤 حسابي ورصيدي", callback_data="my_account")
    btn_promo = InlineKeyboardButton("🎁 كود هدية", callback_data="promo_code")
    btn_ref = InlineKeyboardButton("👥 دعوة أصدقاء (3000 ل.س)", callback_data="referral_link")
    btn_support = InlineKeyboardButton("📞 الدعم الفني", callback_data="support_chat")
    
    markup.add(btn_play)
    markup.add(btn_deposit, btn_withdraw)
    markup.add(btn_account, btn_promo)
    markup.add(btn_ref, btn_support)
    
    # لوحة تحكم الآدمن تظهر فقط للآدمن
    if chat_id == ADMIN_ID:
        btn_admin = InlineKeyboardButton("🛠️ لوحة تحكم الآدمن", callback_data="admin_panel")
        markup.add(btn_admin)
    
    welcome_text = (
        "🐊 **أهلاً بك في Valo Croco Bot!** 🎰\n\n"
        "عالم الحظ، التحدي، والأرباح الكبيرة في انتظارك! الحد الأدنى للإيداع 20,000 ل.س مع بونص 15%.\n\n"
        "اختر أحد الخيارات أدناه للبدء:"
    )
    
    bot.send_message(chat_id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    if call.data == "check_subscription":
        if check_sub(user_id):
            bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح!")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تقم بالاشتراك بعد!", show_alert=True)
            
    elif call.data == "deposit_menu":
        text = (
            "💰 **شحن الرصيد:**\n"
            "• الحد الأدنى للإيداع: **20,000 ليرة سورية**.\n"
            "• البونص على الشحن: **15%**.\n\n"
            "يرجى التحويل حصراً إلى:\n"
            "📲 **سيريتل كاش:** `21938770`\n"
            "*(قريباً سيتم توفير شام كاش سوري و دولار)*\n\n"
            "بعد التحويل، أرسل صورة الإيصال أو رقم الحوالة هنا أو تواصل مع الدعم الفني لتأكيد رصيدك."
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        
    elif call.data == "withdraw_menu":
        text = (
            "💳 **سحب الأرباح:**\n"
            "• الحد الأدنى للسحب: **50,000 ليرة سورية**.\n"
            "• تنويه: يشترط استيفاء خوارزمية اللعب قبل إتمام السحب.\n\n"
            "لطلب السحب، يرجى كتابة رسالة للدعم الفني تتضمن وسيلة السحب ورقمك."
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        
    elif call.data == "my_account":
        text = (
            "👤 **معلومات حسابك:**\n"
            f"• الآيدي: `{user_id}`\n"
            "• الرصيد الحالي: `0` ليرة سورية\n"
            "• الأرباح القابلة للسحب: `0` ليرة سورية"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        
    elif call.data == "referral_link":
        ref_link = f"https://t.me/ValoCrocoBot?start=ref_{user_id}"
        text = (
            "👥 **نظام دعوة الأصدقاء:**\n"
            "احصل على **3,000 ليرة سورية** عن كل صديق تدعوه ويقوم بالتفعيل!\n\n"
            f"🔗 رابط الدعوة الخاص بك:\n`{ref_link}`"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        
    elif call.data == "support_chat":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📞 **الدعم الفني:**\nاكتب رسالتك الآن وسيقوم فريق الدعم بالرد عليك في أقرب وقت.")
        
    elif call.data == "admin_panel" and user_id == ADMIN_ID:
        text = (
            "🛠️ **لوحة تحكم الآدمن:**\n\n"
            "• إجمالي إيداعات اليوم: `0 ل.س`\n"
            "• طلبات السحب المعلقة: `0`\n"
            "• رسائل الدعم الفني: `لا توجد رسائل جديدة`"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

print("Valo Croco Bot is running successfully...")
bot.infinity_polling()
