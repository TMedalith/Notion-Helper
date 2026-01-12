from notion_client import Client
import logging
from bot.models import Opportunity

logger = logging.getLogger(__name__)

class NotionRepository:
    def __init__(self, token: str, db_id:str):
        self.client = Client(auth=token)
        self.db_id= db_id

    def save(self, opportunity: Opportunity)->bool:
        try:
            page_data = {
                "parent": {"database_id": self.db_id},
                "properties": opportunity.to_notion()
            }
            
            # Agregar descripción como contenido de la página
            if opportunity.description:
                page_data["children"] = [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": opportunity.description}}]
                        }
                    }
                ]
            
            self.client.pages.create(**page_data)
            logger.info(f"Saved: {opportunity.name}")
            return True
        except Exception as e:
            logger.error(f"Save error: {e}")   
            return False 


