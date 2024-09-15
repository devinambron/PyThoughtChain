import os
from dotenv import load_dotenv
from app.services.chat_service import chat

load_dotenv()

if __name__ == '__main__':
    chat()