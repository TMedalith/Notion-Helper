
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_TOKEN= os.getenv("TELEGRAM_TOKEN", "")
    NOTION_TOKEN=os.getenv("NOTION_TOKEN", "")
    DATABASE_ID = os.getenv("DATABASE_ID", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    #agregar validacion de existencia.