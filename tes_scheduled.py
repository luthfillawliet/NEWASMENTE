import asyncio
import telegram
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import schedule
import time
from datetime import datetime
import pytz

# Define your bot token and chat ID
TOKEN = '7389606593:AAGTPGLXb_AAzUalaaxDWo8Wwgq5DF1akXE'
CHAT_ID = '1029804860'

# Create the bot
bot = Bot(token=TOKEN)

# Function to send a message
async def send_message():
    await bot.send_message(chat_id=CHAT_ID, text="This is your scheduled message!")

# Function to schedule the message
def schedule_message():
    tz = pytz.timezone('Asia/Singapore')  # Timezone UTC+8
    schedule_time = datetime.now(tz).replace(hour=17, minute=2, second=0, microsecond=0)
    now = datetime.now(tz)

    if schedule_time < now:
        schedule_time = schedule_time.replace(day=now.day + 1)
    
    delay = (schedule_time - now).total_seconds()
    print(f"Message scheduled in {delay} seconds")
    schedule.every(delay).seconds.do(lambda: asyncio.run(send_message()))

# Function to keep running the schedule
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    schedule_message()
    run_schedule()
