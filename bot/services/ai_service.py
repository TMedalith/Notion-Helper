
import json
import logging
from typing import Optional
from groq import Groq
from bot.constants import EXTRACTION_PROMPT
from bot.models import Opportunity
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, api_key:str):
        self.client = Groq(api_key=api_key)

    def analize(self, text: str) -> Optional[Opportunity]:
        prompt = EXTRACTION_PROMPT.format(text=text)
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a JSON extraction assistant. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            content = response.choices[0].message.content.strip()
            
            # Limpiar markdown code blocks si existen
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:].strip()
            
            data = json.loads(content)
            return Opportunity.from_dict(data)
        except Exception as a:
            logger.error(f"Error: {a}")  
            return None 
        
    