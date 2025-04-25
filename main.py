
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id] = {'step': 1}
    await update.message.reply_text("Salom! Buyurtma uchun manzilingizni yozing:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_data:
        user_data[chat_id] = {'step': 1}

    step = user_data[chat_id]['step']

    if step == 1:
        user_data[chat_id]['address'] = text
        user_data[chat_id]['step'] = 2
        await update.message.reply_text("📞 Telefon raqamingizni kiriting:")
    elif step == 2:
        user_data[chat_id]['phone'] = text
        user_data[chat_id]['step'] = 3
        await update.message.reply_text("💊 Qanday dorilar kerak?")
    elif step == 3:
        user_data[chat_id]['meds'] = text
        await update.message.reply_text("✅ Buyurtma qabul qilindi!\n\n📍 Manzil: {}\n📞 Telefon: {}\n💊 Dorilar: {}\n\nOperatorlar tez orada siz bilan bog‘lanadi.".format(
            user_data[chat_id]['address'], user_data[chat_id]['phone'], user_data[chat_id]['meds']
        ))
        user_data[chat_id]['step'] = 1

app = ApplicationBuilder().token("7873784574:AAFeLaGFCmRa3ILJIfOpbBetQaN-8BMS8H0").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
