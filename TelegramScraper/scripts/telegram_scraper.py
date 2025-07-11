import os
from datetime import datetime
import json
import logging
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='log/telegram_scraper.log'
)

# Load environment variables
load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

# Target channels
CHANNELS = [
    'CheMed123',
    'lobelia4cosmetics',
    'tikvahpharma'
]

# Data lake directory structure
BASE_DIR = 'data/raw'
os.makedirs(BASE_DIR, exist_ok=True)

async def scrape_channel(client, channel_name):
    """Scrape messages and images from a Telegram channel"""
    try:
        logging.info(f"Starting scrape for channel: {channel_name}")
        
        # Create directory structure
        date_str = datetime.now().strftime('%Y-%m-%d')
        channel_dir = os.path.join(BASE_DIR, 'telegram_messages', date_str, channel_name)
        images_dir = os.path.join(BASE_DIR, 'telegram_images', date_str, channel_name)
        os.makedirs(channel_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)
        
        # File paths
        messages_file = os.path.join(channel_dir, 'messages.json')
        images_list_file = os.path.join(channel_dir, 'images_metadata.json')
        
        messages_data = []
        images_data = []
        
        async for message in client.iter_messages(channel_name, limit=10):
            # Skip if message is empty
            if not message:
                continue
                
            message_dict = {
                'id': message.id,
                'date': message.date.isoformat(),
                'text': message.text,
                'views': message.views,
                'forwards': message.forwards,
                'replies': message.replies and message.replies.replies,
            }
            messages_data.append(message_dict)
            
            # Handle images
            if isinstance(message.media, MessageMediaPhoto):
                image_path = os.path.join(images_dir, f'{message.id}.jpg')
                await client.download_media(message.media, file=image_path)
                
                images_data.append({
                    'message_id': message.id,
                    'image_path': image_path,
                    'date': message.date.isoformat(),
                    'caption': message.text
                })
        
        # Save messages to JSON
        with open(messages_file, 'w', encoding='utf-8') as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)
            
        # Save images metadata
        with open(images_list_file, 'w', encoding='utf-8') as f:
            json.dump(images_data, f, ensure_ascii=False, indent=2)
            
        logging.info(f"Successfully scraped {len(messages_data)} messages from {channel_name}")
        
    except Exception as e:
        logging.error(f"Error scraping channel {channel_name}: {str(e)}")

async def main():
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(PHONE_NUMBER)
    
    for channel in CHANNELS:
        await scrape_channel(client, channel)
    
    await client.disconnect()

asyncio.run(main())