import datetime  # Import the datetime library
import schedule
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

def scheduled_task(context: ContextTypes.DEFAULT_TYPE):
  """
  This function defines the task logic to be executed at the scheduled time.

  Args:
      context (ContextTypes.DEFAULT_TYPE): Context object provided by the Telegram Bot API
          (optional, if you need interaction functionalities).
  """

  # Your task logic here, using the context argument if needed
  chat_id = 1029804860  # Replace with your chat ID
  message = "This is a scheduled message!"

  if context:  # Check if context is available (optional)
      context.bot.send_message(chat_id=chat_id, text=message)
  else:
      # Implement alternative message sending logic without context (e.g., using your API)
      send_message(chat_id, message)  # Assuming you have a send_message function

  def send_message(chat_id, message):
      # Your implementation to send the message using your bot API (e.g., requests library)
      # Replace with your actual API call
      print(f"Sending message to chat ID {chat_id}: {message}")  # Placeholder for now

def get_sg_time():
  """
  Calculates the delay for scheduling the task at 22:13 Singapore Time (SGT).

  Returns:
      float: Delay in seconds from current time to SGT 22:13.
  """

  now = datetime.now()  # Use datetime.now() after importing datetime
  sg_offset = timedelta(hours=8)  # UTC+8 for Singapore Time
  target_datetime = datetime(year=now.year, month=now.month, day=now.day, hour=22, minute=13) + sg_offset
  delay = (target_datetime - now).total_seconds()
  return delay

def main():
  """
  Main function that starts the scheduling process.

  Options:
      1. Thread-based scheduling (recommended)
      2. Blocking scheduling (not recommended for long-running tasks)
  """

  # Choose either thread-based or blocking scheduling based on your needs:

  # 1. Thread-based scheduling (recommended)
  delay = get_sg_time()
  t = threading.Timer(delay, scheduled_task)
  t.start()

  # 2. Blocking scheduling (not recommended) - comment out thread-based code above if using this
  # delay = get_sg_time()
  # schedule.every().day.at("22:13").do(scheduled_task)
  # while True:
  #     schedule.run_pending()
  #     schedule.sleep(1)

if __name__ == "__main__":
  main()
