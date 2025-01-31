import os
from telethon import TelegramClient
from dotenv import load_dotenv
import re

load_dotenv(dotenv_path='session/secrets.env')

# API credentials
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
channel_username = os.getenv("CHANNEL_USERNAME")

# Dir to save PDFs
pdf_dir = "pdfs"
os.makedirs(pdf_dir, exist_ok=True)

# Session Dir
session_dir = "session"
os.makedirs(session_dir, exist_ok=True)  
session_file = os.path.join(session_dir, "session_name")

# Client initialization
client = TelegramClient(session_file, api_id, api_hash)
client.download_chunk_size = 1024 * 1024 

def sanitize_filename(filename):
    """Remove invalid characters from the filename for Windows compatibility."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

async def fetch_pdfs():
    await client.start()
    async for message in client.iter_messages(channel_username):
        if message.document and message.document.mime_type == "application/pdf":
            file_name = message.document.attributes[0].file_name
            file_name = sanitize_filename(file_name)
            file_path = os.path.join(pdf_dir, file_name)
            if os.path.exists(file_path):
                print(f"Skipped: {file_name} (already exists)")
                continue
            await message.download_media(file_path)
            print(f"Downloaded: {file_name}")

client.loop.run_until_complete(fetch_pdfs())
