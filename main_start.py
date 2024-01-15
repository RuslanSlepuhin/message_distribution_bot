import asyncio

from bot_view.bot import HorecaBot
from bot_view.teleth_bot import TelethBot

def tg_bot_init():
    bot = HorecaBot()
    bot.bot_handlers()

def teleth_bot_init():
    teleth_bot = TelethBot()
    teleth_bot.init_bot()
    # loop.
    # loop.run_until_complete(teleth_bot.init_bot())

if __name__ == "__main__":
    # teleth_bot_init()
    tg_bot_init()
