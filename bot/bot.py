import sys
import argparse
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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
from bot.config import config

# Telegram Command Handlers (Transport Layer)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_start(update.effective_user.id)
    await update.message.reply_text(response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_help()
    await update.message.reply_text(response)

async def health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_health()
    await update.message.reply_text(response)

async def labs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_labs()
    await update.message.reply_text(response)

async def scores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lab_id = "".join(context.args) if context.args else None
    response = await handle_scores(lab_id)
    await update.message.reply_text(response)

# Test Mode Interface
async def test_mode(query: str):
    """Offline test mode to verify handler logic without Telegram."""
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
        print(f"Unknown command: {cmd}")

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

    print("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
