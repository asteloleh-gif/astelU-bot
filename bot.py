import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
CONTACT_USERNAME = "astel_u"

# Всі тексти та посилання по мовах
LANGS = {
    "ua": {
        "title": "🇺🇦 Українська",
        "channel": "https://t.me/astel_ua",
        "chat": "https://t.me/astel_ua_chat",
        "submenu_title": "🇺🇦 Вітаю!\n\nКуди хочеш перейти?",
        "btn_channel": "📢 Канал",
        "btn_chat": "💬 Чат",
        "btn_back": "⬅️ Назад",
        "btn_contact": "💰 Співпраця",
    },
    "en": {
        "title": "🌎 English",
        "channel": "https://t.me/astel_en",
        "chat": "https://t.me/astel_en_chat",
        "submenu_title": "🌎 Hello!\n\nWhere would you like to go?",
        "btn_channel": "📢 Channel",
        "btn_chat": "💬 Chat",
        "btn_back": "⬅️ Back",
        "btn_contact": "💰 Cooperation",
    },
}

WELCOME_TITLE = "🔥 *Welcome to Astel*"

WELCOME_SUB = (
    "Building an e-commerce business in the USA.\n\n"
    "Choose your language:"
)

WELCOME_CONTACT_BTN = "💰 Cooperation"


def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton(data["title"], callback_data=key)]
        for key, data in LANGS.items()
    ]

    keyboard.append(
        [
            InlineKeyboardButton(
                WELCOME_CONTACT_BTN,
                url=f"https://t.me/{CONTACT_USERNAME}",
            )
        ]
    )

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

    data = LANGS[query.data]

    keyboard = [
        [InlineKeyboardButton(data["btn_channel"], url=data["channel"])],
        [InlineKeyboardButton(data["btn_chat"], url=data["chat"])],
        [InlineKeyboardButton(data["btn_contact"], url=f"https://t.me/{CONTACT_USERNAME}")],
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

    print("Bot started.")

    app.run_polling()


if __name__ == "__main__":
    main()
