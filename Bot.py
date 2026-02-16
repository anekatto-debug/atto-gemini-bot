import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import google.generativeai as genai

TOKEN = os.getenv('BOT_TOKEN')
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash',
    system_instruction="Tu es l'agent IA d'Atto. Gaming/anime/code/fitness/content. Dis toujours 'Je suis l'agent IA d'Atto'. Par Atto.")

user_histories = {}

async def start(update, context):
    await update.message.reply_text("🚀 Je suis l'agent IA d'Atto ! Par Atto.")

async def chat(update, context):
    uid = update.effective_user.id
    if uid not in user_histories:
        user_histories[uid] = []
    msg = update.message.text
    user_histories[uid].append({"role": "user", "parts": [msg]})
    try:
        resp = model.generate_content(user_histories[uid])
        await update.message.reply_text(resp.text)
        user_histories[uid].append({"role": "model", "parts": [resp.text]})
        if len(user_histories[uid]) > 20:
            user_histories[uid] = user_histories[uid][-10:]
    except Exception as e:
        await update.message.reply_text(f"Erreur Atto : {e}")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Atto bot démarré !")
    app.run_polling()
