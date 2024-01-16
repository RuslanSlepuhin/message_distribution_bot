import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from bot_view.bot_methods import Methods
from variables import variables

config = configparser.ConfigParser()
config.read("./settings/config.ini")

class HorecaBot:

    def __init__(self, token=None):
        self.token = token if token else config['Bot']['token']
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.superusers = config["Admins"]["superuser"].split(",")
        self.admins = config["Admins"]["admin"].split(",")
        self.methods = Methods(self)
        self.callbacks = []
        self.receive_distribution_excel = False
        self.distribution_pull_ids = []
        self.message = None

    class ChannelForm(StatesGroup):
        channel = State()

    class DistributionMessageForm(StatesGroup):
        distribution_message = State()

    def bot_handlers(self):

        @self.dp.message_handler(state=self.DistributionMessageForm.distribution_message)
        async def distribution_message(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['distribution_message'] = message.text
                distribution_message = message.text
            await state.finish()
            self.message = message
            distribution_result = await self.methods.distribution(id_list=self.distribution_pull_ids, message_text=distribution_message)
            if distribution_result:
                await self.bot.send_message(message.chat.id, variables.distribution_was_success)
            else:
                await self.bot.send_message(message.chat.id, variables.distribution_was_broken)

        @self.dp.message_handler(state=self.ChannelForm.channel)
        async def channel(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['channel'] = message.text
                channel = message.text
            await state.finish()
            await self.methods.get_external_subscribers(message, channel)

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            text = "Меню Суперюзера"
            self.callbacks = await self.methods.send_message_inline_keyboard(message, buttons=variables.superuser_start_buttons, text=text, row=1)

        @self.dp.message_handler(commands=['report'])
        async def report(message: types.Message):
            await self.methods.send_file(message, "./media/excel/sending_report.xlsx")

        @self.dp.callback_query_handler()
        async def callbacks(callback: types.CallbackQuery):
            if callback.data in self.callbacks:
                match callback.data:
                    case "get_external_subscribers": await self.get_external_subscribers(callback.message)
                    case "get_own_contacts": await self.methods.get_own_contacts(callback.message)
                    case "distribution":
                        await self.bot.send_message(callback.message.chat.id, variables.distribution_message)
                        self.receive_distribution_excel = True

        @self.dp.message_handler(content_types=['document'])
        async def download_doc(message: types.Message):
            if self.receive_distribution_excel:
                self.distribution_pull_ids = await self.methods.receive_excel(message)
                await self.DistributionMessageForm.distribution_message.set()
                await self.bot.send_message(message.chat.id, variables.distribution_request)
            else:
                await self.bot.send_message(message.chat.id, variables.restricted_message)

        executor.start_polling(self.dp, skip_updates=True)

    async def get_external_subscribers(self, message):
        await self.ChannelForm.channel.set()
        await self.bot.send_message(message.chat.id, variables.get_external_subscribers)

