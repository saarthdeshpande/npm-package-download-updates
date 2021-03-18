import requests
import telebot
import pandas as pd
from datetime import datetime, timedelta
import weasyprint as wsp
import PIL as pil
import os

TOKEN = <YOUR_TELEGRAM_BOT_TOKEN>
PACKAGE_NAME = <YOUR_NPM_PACKAGE_NAME>
TELEGRAM_CHAT_ID = <YOUR_TELEGRAM_CHAT_ID> # to find your chat_id, refer: https://stackoverflow.com/a/37396871

bot = telebot.TeleBot(token=TOKEN)


def trim(source_filepath, target_filepath=None, background=None):
    if not target_filepath:
        target_filepath = source_filepath
    img = pil.Image.open(source_filepath)
    if background is None:
        background = img.getpixel((0, 0))
    border = pil.Image.new(img.mode, img.size, background)
    diff = pil.ImageChops.difference(img, border)
    bbox = diff.getbbox()
    img = img.crop(bbox) if bbox else img
    img.save(target_filepath)


if __name__ == '__main__':
    img_filepath = 'npmjs_updates.png'
    css = wsp.CSS(string='''
    @page { size: 2048px 2048px; padding: 0px; margin: 0px; }
    table, td, tr, th { border: 1px solid black; }
    td, th { padding: 4px 8px; }
    ''')

    url = f"https://api.npmjs.org/downloads/range/{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')}:{datetime.now().strftime('%Y-%m-%d')}/{PACKAGE_NAME}"

    downloads = pd.DataFrame(requests.get(url).json()['downloads'])

    downloads = downloads[['day', 'downloads']]

    html = wsp.HTML(string=downloads.to_html())
    html.write_png(img_filepath, stylesheets=[css])
    trim(img_filepath)
    bot.send_photo(TELEGRAM_CHAT_ID, open(img_filepath, 'rb'))
    os.remove(img_filepath)
