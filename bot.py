import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
CONTACT_USERNAME = "astel_u"

# Всі тексти та посилання по мовах
LANGS = {
    "ua": {
        "title": "Вітаю",
        "channel": "https://t.me/astel_ua",
        "chat": "https://t.me/astel_ua_chat",
        "submenu_title": "Вітаю 👋 Куди хочеш перейти?",
        "btn_channel": "📢 Канал",
        "btn_chat": "💬 Чат",
        "btn_back": "⬅️ Назад",
        "btn_contact": "💰 Співпраця",
    },
    "en": {
        "title": "Hello",
        "channel": "https://t.me/astel_en",
        "chat": "https://t.me/astel_en_chat",
        "submenu_title": "Hello 👋 Where would you like to go?",
        "btn_channel": "📢 Channel",
        "btn_chat": "💬 Chat",
        "btn_back": "⬅️ Back",
        "btn_contact": "💰 Cooperation",
    },
}

WELCOME_TITLE = "🔥 *Ласкаво просимо в Astel / Welcome to Astel*"
WELCOME_SUB = (
    "Тут тільки по справі — новини, рух і спілкування.\n"
    "Оберіть мову / регіон:\n\n"
    "Here it's business only — news, movement, and community.\n"
    "Choose your language / region:"
)
WELCOME_CONTACT_BTN = "💰 Співпраця / Cooperation"


def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton(data["title"], callback_data=key)]
        for key, data in LANGS.items()
    ]
    keyboard.append([InlineKeyboardButton(WELCOME_CONTACT_BTN, url=f"https://t.me/{CONTACT_USERNAME}")])
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{WELCOME_TITLE}\n\n{WELCOME_SUB}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


async def language_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    key = query.data
    data = LANGS[key]

    keyboard = [
        [InlineKeyboardButton(data["btn_channel"], url=data["channel"])],
        [InlineKeyboardButton(data["btn_chat"], url=data["chat"])],
        [InlineKeyboardButton(data["btn_back"], callback_data="back")],
    ]
    await query.edit_message_text(
        data["submenu_title"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        f"{WELCOME_TITLE}\n\n{WELCOME_SUB}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern="^back$"))
    app.add_handler(CallbackQueryHandler(language_chosen, pattern="^(ua|en)$"))

    print("Бот запущено. Зупинити через Ctrl+C.")
    app.run_polling()


if name == "__main__":
    main()
