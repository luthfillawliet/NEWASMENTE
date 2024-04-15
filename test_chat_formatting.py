important_word = "important"
bot_response = f"This message contains an {important_word} word."
update.message.reply_text(bot_response, parse_mode=telegram.ext.ParseMode.MARKDOWNV2)