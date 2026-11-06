import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "9294468427:AAGOHNplOfxQBdoTRSaxOb4mp0lzo_-mrOA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=2)
    
    btn_play = InlineKeyboardButton("🎮 العب الآن", web_app=telebot.types.WebAppInfo(url="https://google.com"))
    btn_deposit = InlineKeyboardButton("💰 شحن الرصيد", callback_data="deposit")
    btn_withdraw = InlineKeyboardButton("💳 سحب الأرباح", callback_data="withdraw")
    btn_account = InlineKeyboardButton("👤 حسابي ورصيدي", callback_data="account")
    btn_promo = InlineKeyboardButton("🎁 كود هدية", callback_data="promo")
    btn_ref = InlineKeyboardButton("👥 دعوة أصدقاء", callback_data="referral")
    
    markup.add(btn_play)
    markup.add(btn_deposit, btn_withdraw)
    markup.add(btn_account, btn_promo)
    markup.add(btn_ref)
    
    welcome_text = (
        "🐊 **أهلاً بك في Valo Croco Bot!** 🎰\n\n"
        "عالم الحظ، التحدي، والأرباح الكبيرة في انتظارك! العب الآن، اضاعف رصيدك، واسحب أرباحك بكل سهولة.\n\n"
        "اختر أحد الخيارات أدناه للبدء:"
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

print("Valo Croco Bot is running...")
bot.infinity_polling()
