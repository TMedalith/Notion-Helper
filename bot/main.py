from telegram import Update
from telegram.ext import MessageHandler, filters, ApplicationBuilder, ConversationHandler, CommandHandler
import logging

from bot.constants import State

from bot.config import Config
from bot.handlers.register_handler import RegistrationHandler
from bot.repositories.notion_repository import NotionRepository
from bot.services.ai_service import AIService

logger = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_bot():

    ai = AIService(Config.GROQ_API_KEY)
    repo = NotionRepository(Config.NOTION_TOKEN, Config.DATABASE_ID)
    handler = RegistrationHandler(ai, repo)
    
    app = ApplicationBuilder().token(Config.TELEGRAM_TOKEN).build()



    conversation = ConversationHandler(
        entry_points=[
            CommandHandler("new", handler.start)
            ],
        states={
            State.WAITING_TEXT:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler.process)
            ],
            State.CONFIRMING:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler.confirm)
            ]
        },
        fallbacks=[],

    )

    app.add_handler(conversation)
    return app


def main():
    bot = create_bot()
    logger.info("Bot started YEIIII")
    bot.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()