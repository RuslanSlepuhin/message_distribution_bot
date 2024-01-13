import asyncio
import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
config = configparser.ConfigParser()
config.read("./settings/config.ini")

class HorecaBot:

    def __init__(self, token=None):
        self.token = token if token else config['Bot']['token']
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())

    def bot_handlers(self):

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            try:
                await self.bot.send_message(5502797471, f"id is {message.chat.id}")
            except Exception as ex:
                print(ex)
            pass

        @self.dp.message_handler(commands=['subscribers'])
        async def start(message: types.Message):
            from bot_view.teleth_bot import TelethBot
            teleth_bot = TelethBot()
            client = asyncio.run(teleth_bot.init_bot())
            asyncio.run(teleth_bot.get_subscribers())

        @self.dp.callback_query_handler()
        async def callbacks(callback: types.CallbackQuery):
            pass

        @self.dp.message_handler(content_types=['text'])
        async def text_message(message):
            pass

        executor.start_polling(self.dp, skip_updates=True)