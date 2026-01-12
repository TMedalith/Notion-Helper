
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.constants import State
from bot.repositories.notion_repository import NotionRepository
from bot.services.ai_service import AIService


class RegistrationHandler:
    def __init__(self, ai_parser:AIService, repo: NotionRepository):
        self.ai = ai_parser
        self.repo = repo

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "NTP yo lo guardo en notion. Pasa el dato :D"
        )  
        return State.WAITING_TEXT
    async def process(self, update:Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Analizanding...") 

        opportunity = self.ai.analize(update.message.text)

        if opportunity is None:
            await update.message.reply_text(
                "Error al analizar. Intenta de nuevo más tarde o verifica tu API key de Gemini."
            )
            context.user_data.clear()
            return ConversationHandler.END

        context.user_data["opportunity"] = opportunity

        summary = (
            f"📝 **{opportunity.name}**\n"
            f"📅 Deadline: {opportunity.deadline}\n"
            f"🏷️ Tags: {', '.join(opportunity.tags)}\n"
            f"🔗 Link: {opportunity.link or 'N/A'}\n\n"
            f"Ta bien? (si/no)"
        )
        await update.message.reply_text(summary, parse_mode='Markdown')
        return State.CONFIRMING
    
    async def confirm(self, update:Update, context: ContextTypes.DEFAULT_TYPE):
        response = update.message.text.lower()
        if response not in ["si", "no"]:
            await update.message.reply_text("No reconocido. Usa /new again")
            context.user_data.clear()
            return ConversationHandler.END
        
        opportunity = context.user_data.get("opportunity")
        
        if opportunity is None:
            await update.message.reply_text("Error: No pude procesar la información. Intenta de nuevo con /new")
            context.user_data.clear()
            return ConversationHandler.END

        if response == "no":
            await update.message.reply_text("Cancelado. Usa /new para intentar de nuevo")
            context.user_data.clear()
            return ConversationHandler.END

        if self.repo.save(opportunity):
            await update.message.reply_text("Listop")
        else:
            await update.message.reply_text("ups, no se guardo")

        context.user_data.clear()
        return ConversationHandler.END    