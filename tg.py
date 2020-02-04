import os
import telegram


tg_token = os.environ['TG_TOKEN']
tg_chat_id = os.environ['TG_CHAT_ID']


def send_text(msg):
    bot = telegram.Bot(token=tg_token)
    bot.send_message(
        chat_id=tg_chat_id,
        text=msg,
        parse_mode=telegram.ParseMode.HTML,
    )
