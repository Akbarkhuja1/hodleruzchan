import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@HodlerUz"

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

def get_top_10_coins():
    url = "https://api.coinpaprika.com/v1/tickers"
    response = requests.get(url)
    coins = response.json()
    top_10 = sorted(coins, key=lambda x: x["rank"])[:10]
    message = "<b>Top 10 kripto kurslari:</b>
"
    for coin in top_10:
        message += f"{coin['name']} ({coin['symbol']}): ${coin['quotes']['USD']['price']:.2f}
"
    message += "\nTo‘liq ro‘yxat: https://coinpaprika.com"
    return message

async def send_price():
    text = get_top_10_coins()
    await bot.send_message(CHANNEL_ID, text)

async def main():
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
    scheduler.add_job(send_price, "cron", hour=8, minute=0)
    scheduler.add_job(send_price, "cron", hour=20, minute=0)
    scheduler.start()
    print("Bot ishga tushdi")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
