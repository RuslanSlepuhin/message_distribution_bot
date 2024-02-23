import asyncio
from multiprocessing import Process

from bot_view.bot import DisributionBot
from bot_view.teleth_bot import TelethBot
from coffee_bot.your_coffee_bot import YourCoffeeBot


def tg_bot_init():
    bot = DisributionBot()
    bot.bot_handlers()

def teleth_bot_init():
    teleth_bot = TelethBot()
    teleth_bot.init_bot()

def your_coffee_bot():
    coffee_bot = YourCoffeeBot()
    coffee_bot.bot_handlers()

if __name__ == "__main__":
    process0 = Process(target=teleth_bot_init)
    process0.start()
    process0.join()

    # process1 = Process(target=tg_bot_init)
    # process2 = Process(target=your_coffee_bot)

    # process1.start()
    # process2.start()

    # process1.join()
    # process2.join()