import sys
import argparse
import os
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Ensure the parent directory is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from bot.handlers.commands import (
    handle_start, 
    handle_help, 
    handle_health, 
    handle_labs, 
    handle_scores
)
from bot.handlers.router import route_intent
from bot.config import config

# Telegram Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_start(update.effective_user.id)
    keyboard = [[InlineKeyboardButton("More Info", callback_data="more_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(response, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_help()
    keyboard = [[InlineKeyboardButton("More Info", callback_data="more_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(response, reply_markup=reply_markup)

async def health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_health()
    keyboard = [[InlineKeyboardButton("More Info", callback_data="more_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(response, reply_markup=reply_markup)

async def labs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_labs()
    keyboard = [[InlineKeyboardButton("More Info", callback_data="more_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(response, reply_markup=reply_markup)

async def scores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lab_id = "".join(context.args) if context.args else None
    response = await handle_scores(lab_id)
    keyboard = [[InlineKeyboardButton("More Info", callback_data="more_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(response, reply_markup=reply_markup)

# Plain text message handler (LLM Router)
async def plain_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = await route_intent(user_text)
    keyboard = [[InlineKeyboardButton("More Info", callback_data="more_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(response, reply_markup=reply_markup)

# Test Mode Interface
async def test_mode(query: str):
    """Offline test mode to verify handler logic without Telegram."""
    if query.startswith('/'):
        parts = query.split()
        cmd = parts[0].lstrip('/')
        args = parts[1:]
        
        if cmd == "start":
            print(await handle_start())
        elif cmd == "help":
            print(await handle_help())
        elif cmd == "health":
            print(await handle_health())
        elif cmd == "labs":
            print(await handle_labs())
        elif cmd == "scores":
            lab_id = args[0] if args else None
            print(await handle_scores(lab_id))
        else:
            print(await route_intent(query))
    else:
        print(await route_intent(query))

def main():
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument("--test", type=str, help="Run a command in test mode and exit")
    args = parser.parse_args()

    if args.test:
        asyncio.run(test_mode(args.test))
        sys.exit(0)

    # Production Telegram Loop
    if config.BOT_TOKEN == "placeholder_token":
        print("Error: BOT_TOKEN not set in .env.bot.secret")
        sys.exit(1)
        
    application = Application.builder().token(config.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("health", health))
    application.add_handler(CommandHandler("labs", labs_command))
    application.add_handler(CommandHandler("scores", scores))
    
    # Handle all non-command text with the LLM router
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), plain_text_handler))

    print("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
