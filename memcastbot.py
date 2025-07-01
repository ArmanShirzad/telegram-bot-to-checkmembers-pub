from groqsupport import GroqSupport
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from configure import Store

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize your bot with your bot token
TOKEN = Store.MEMOCAST_BOT
CHANNEL_USERNAME = Store.CHANNEL_USERNAME  # Without @
ADMIN_CHAT_ID = Store.ADMIN_CHAT_ID  # Replace with your actual admin chat ID
translator = GroqSupport(Store.GROQ_API_KEY)

# Define messages
MESSAGES = {
    "welcome": {
        "en": "Welcome! Choose an option below:",
        "fa": "خوش آمدید! گزینه زیر را انتخاب کنید:"
    },
    "join_prompt": {
        "en": "To access the resources, you need to join our channel. Click the button below to proceed:",
        "fa": "برای دسترسی به منابع، لازم است به کانال ما بپیوندید. برای ادامه، روی دکمه زیر کلیک کنید:"
    },
    "join_instructions": {
        "en": "Click the button below to join our channel. After joining, click 'I have joined'.",
        "fa": "برای عضویت در کانال ما روی دکمه زیر کلیک کنید. پس از عضویت، روی 'من عضو شدم' کلیک کنید."
    },
    "membership_confirmed": {
        "en": "You're a member! Welcome to the channel.",
        "fa": "شما عضو هستید! به کانال خوش آمدید."
    },
    "membership_required": {
        "en": "Please join the channel first.\n",
        "fa": "لطفاً ابتدا به کانال ما بپیوندید."
    },
    "error_occurred": {
        "en": "An error occurred. Please try again later.",
        "fa": "خطایی رخ داده است. لطفاً بعداً دوباره تلاش کنید."
    },
    "meditation_starting": {
        "en": "Starting your meditation session...",
        "fa": "در حال شروع جلسه مدیتیشن شما..."
    },
    "meditation_completed": {
        "en": "Meditation session completed!",
        "fa": "جلسه مدیتیشن به پایان رسید!"
    },
    "help_text": {
        "en": "Here is the help information:\n"
              "/start - Start the bot\n"
              "/meditate - Start meditation\n"
              "/help - Get help\n"
              "/feedback - Send feedback",
        "fa": "اینجا راهنمایی ها را مشاهده می‌کنید:\n"
              "/start - شروع ربات\n"
              "/meditate - شروع مدیتیشن\n"
              "/help - دریافت راهنما\n"
              "/feedback - ارسال بازخورد"
    },
    "feedback_prompt": {
        "en": "Please send your feedback. I'll forward it to the admins.",
        "fa": "لطفاً بازخورد خود را ارسال کنید. آن را به مدیران ارسال خواهم کرد."
    },
    "feedback_received": {
        "en": "Thank you for your feedback!",
        "fa": "متشکرم برای بازخورد شما!"
    },
    "feedback_forward": {
        "en": "Feedback from @{username} ({user_id}):\n{feedback}",
        "fa": "بازخورد از @{username} ({user_id}):\n{feedback}"
    },
    "start_meditation_instruction": {
        "en": "Starting your meditation session. Please find a quiet place and relax.",
        "fa": "شروع جلسه مدیتیشن شما. لطفاً جای آرامی پیدا کنید و آرامش یابید."
    },
}

async def is_user_member(bot, channel_username: str, user_id: int) -> bool:
    """
    Check if a user is a member of a specified Telegram channel.

    Args:
        bot: The bot instance.
        channel_username (str): The Telegram channel username (without @).
        user_id (int): The Telegram user ID.

    Returns:
        bool: True if the user is a member, False otherwise.
    """
    try:
        member_status = await bot.get_chat_member(
            chat_id=f"@{channel_username}",
            user_id=user_id
        )
        return member_status.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Error checking membership for user {user_id}: {e}")
        return False

# Start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot = context.bot

    is_member = await is_user_member(bot, CHANNEL_USERNAME, user_id)

    if is_member:
        # User is a member
        keyboard = [
            [InlineKeyboardButton("Meditate - Start meditation // شروع مدیتیشن", callback_data="start_meditation")],
            [InlineKeyboardButton("Help // دریافت راهنما", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"{MESSAGES['welcome']['en']}\n{MESSAGES['welcome']['fa']}",
            reply_markup=reply_markup,
        )
    else:
        # User is not a member
        keyboard = [
            [InlineKeyboardButton("Join Channel // عضویت در کانال", callback_data="join_channel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"{MESSAGES['join_prompt']['en']}\n{MESSAGES['join_prompt']['fa']}",
            reply_markup=reply_markup,
        )

# Button Handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    bot = context.bot

    if data == "join_channel":
        # Send the URL button and "I have joined" button
        keyboard = [
            [InlineKeyboardButton("Join Channel // عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("I have joined // من عضو شدم", callback_data="check_membership")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.answer()
        await query.edit_message_text(
            text=f"{MESSAGES['join_instructions']['en']}\n{MESSAGES['join_instructions']['fa']}",
            reply_markup=reply_markup,
        )

    elif data == "check_membership":
        is_member = await is_user_member(bot, CHANNEL_USERNAME, user_id)

        if is_member:
            await query.answer()
            # Show meditation and help options
            keyboard = [
                [InlineKeyboardButton("Meditate - Start meditation // شروع مدیتیشن", callback_data="start_meditation")],
                [InlineKeyboardButton("Help // دریافت راهنما", callback_data="help")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"{MESSAGES['membership_confirmed']['en']}\n{MESSAGES['membership_confirmed']['fa']}",
                reply_markup=reply_markup,
            )
        else:
            await query.answer(
                text=f"{MESSAGES['membership_required']['en']}\n{MESSAGES['membership_required']['fa']}",
                show_alert=True
            )

    elif data == "start_meditation":
        await query.answer()
        await query.edit_message_text(
            f"{MESSAGES['meditation_starting']['en']}\n{MESSAGES['meditation_starting']['fa']}"
        )
        # Start meditation session
        await meditate_command(update, context)

    elif data == "help":
        await query.answer()
        await query.edit_message_text(
            f"{MESSAGES['help_text']['en']}\n{MESSAGES['help_text']['fa']}"
        )

# Meditation Session Function
async def meditate_command(update, context):
    # Fetch the meditation prompt from Groq (bilingual)
    meditation_text = translator.get_meditation_prompt()
    
    if meditation_text:
        # Format the response message
        response_message = f"🧘‍♂️ Meditation | مدیتیشن: {meditation_text}"  # Assuming the API response is already bilingual
        
        # Check if it's a message or a callback query update
        if update.message:
            chat_id = update.message.chat_id
        else:
            chat_id = update.callback_query.message.chat_id
        
        # Send the meditation text to the user
        try:
            await context.bot.send_message(chat_id=chat_id, text=response_message)
        except Exception as e:
            # Log the error if sending fails
            logging.error(f"Error sending message: {e}")


# Help Command Handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{MESSAGES['help_text']['en']}\n{MESSAGES['help_text']['fa']}"
    )

# Feedback Command Handler
async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{MESSAGES['feedback_prompt']['en']}\n{MESSAGES['feedback_prompt']['fa']}"
    )
    context.user_data['awaiting_feedback'] = True

# Handle Feedback Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_feedback'):
        feedback = update.message.text
        user = update.effective_user

        # Forward feedback to admin
        feedback_text = MESSAGES['feedback_forward']['en'].format(username=user.username or "N/A", user_id=user.id, feedback=feedback) + "\n" + MESSAGES['feedback_forward']['fa'].format(username=user.username or "N/A", user_id=user.id, feedback=feedback)
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=feedback_text
        )

        # Acknowledge receipt
        await update.message.reply_text(
            f"{MESSAGES['feedback_received']['en']}\n{MESSAGES['feedback_received']['fa']}"
        )

        # Reset user state
        context.user_data['awaiting_feedback'] = False

# Error Handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "An unexpected error occurred. Please try again later.\n"
            "یک خطای غیرمنتظره رخ داد. لطفاً بعداً دوباره تلاش کنید."
        )

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("feedback", feedback_command))
    application.add_handler(CommandHandler("meditate", meditate_command))

    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
