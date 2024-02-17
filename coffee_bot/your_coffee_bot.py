import asyncio
import configparser
import random
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor
from coffee_bot.bot_methods import Methods
from coffee_bot import variables
from coffee_bot.menu import main_menu, restart_dialog
from coffee_bot.database_methods import DBMethods

config = configparser.ConfigParser()
config.read("./settings/config.ini")

class YourCoffeeBot:


    def __init__(self, token=None):
        self.token = token if token else config['Bot']['your_coffee_token']
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.superusers = config["Admins"]["superuser"].split(",")
        self.admins = config["Admins"]["admin"].split(",")
        self.methods = Methods(self)
        self.message = None
        self.menu = {}
        self.callback_data = []
        self.db = DBMethods()
        self.db.create_all_tables()
        self.barista_id = self.methods.get_barista_id_list(self.db.select_from(table_name=variables.barista_table_name, data={}, select=True))
        self.order = [] # order way each customer has been written here

    class FreeMessageState(StatesGroup):
        free_message = State()

    class PhoneNumberState(StatesGroup):
        phone_number = State()

    def bot_handlers(self):

        @self.dp.message_handler(state=self.FreeMessageState.free_message)
        async def free_message(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['free_message'] = message.text
                order_data = {
                    variables.user_fields[4]: await self.methods.strfdatetime(),
                    variables.user_fields[6]: message.text
                }
            await state.finish()
            self.db.update(
                variables.user_table_name,
                conditions={variables.user_fields[1]: message.chat.id},
                data=order_data
            )
            await state.finish()
            await self.send_order_to_barista(order_data, message)

        @self.dp.message_handler(state=self.PhoneNumberState.phone_number)
        async def phone_number(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['phone_number'] = message.text
                order_data = {
                    variables.user_fields[3]: ", ".join(self.order),
                    variables.user_fields[4]: await self.methods.strfdatetime(),
                    variables.user_fields[5]: message.text
                }
                self.db.update(
                    variables.user_table_name,
                    conditions={variables.user_fields[1]: message.chat.id},
                    data=order_data
                )
            await state.finish()
            await self.send_order_to_barista(order_data, message)

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            if message.chat.id not in self.barista_id:
                await self.customer_start(message)
            else:
                await self.bot.send_message(message.chat.id, variables.start_barista_message)

        @self.dp.message_handler(commands=['help'])
        async def start(message: types.Message):
            if message.chat.id == variables.superadmin_id:
                await self.bot.send_message(message.chat.id, variables.admin_help)
            else:
                await self.bot.send_message(message.chat.id, variables.user_help)

        @self.dp.message_handler(commands=['get_users'])
        async def get_users(message: types.Message):
            await self.methods.get_users(message)

        @self.dp.message_handler(state='*', commands=['cancel', 'start'])
        @self.dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
        async def cancel_handler(message: types.Message, state: FSMContext):
            current_state = await state.get_state()
            if current_state is None:
                return
            await state.finish()
            await message.reply('ОК')

        @self.dp.message_handler(commands=[variables.add_barista_command])
        async def start(message: types.Message):
            if self.db.insert_into(table_name=variables.barista_table_name, data={variables.barista_fields[1]: message.chat.id}, set_unique=True):
                print("set barista: True")
                self.barista_id.append(message.chat.id)
                await self.bot.send_message(message.chat.id, variables.start_barista_message, reply_markup=ReplyKeyboardRemove())
            else:
                print("set barista: False")

        @self.dp.message_handler(commands=[variables.remove_barista_command])
        async def start(message: types.Message):
            if self.db.delete_data(table_name=variables.barista_table_name, data={variables.barista_fields[1]: message.chat.id}):
                if message.chat.id in self.barista_id:
                    self.barista_id.pop(self.barista_id.index(message.chat.id))
                print("remove barista: True")
                await self.bot.send_message(message.chat.id, variables.remove_barista_message, reply_markup=ReplyKeyboardRemove())
                await self.customer_start(message)

            else:
                print("remove barista: False")

        @self.dp.callback_query_handler()
        async def catch_callback(callback: types.CallbackQuery):
            if callback.data in self.callback_data:
                pass

        @self.dp.message_handler(content_types=['text'])
        async def catch_text(message: types.Message):
            if message.text in self.menu['reply_buttons']:
                if message.text in ["Показать меню"]:
                    await self.methods.send_photo(path=variables.media_path+variables.menu_jpg_path, message=message)

                elif message.text in ["Заказать одним сообщением"]:
                    await self.bot.send_message(message.chat.id, "При отправке сообщения бармену обязательно укажите свой номер телефона для связи с вами. В противном случае мы не можем гарантировать выполнение заказа\n Отмена этого действия /cancel", reply_markup=ReplyKeyboardRemove())
                    await self.FreeMessageState.free_message.set()

                elif message.text in ["Отмена", "<< Назад", "Назад"]:
                    self.order = []
                    self.menu = main_menu
                    await self.methods.send_menu_reply_keyboards(message)

                elif message.text == "Заказать еще":
                    await self.customer_start(message)

                else:
                    self.order.append(message.text)
                    print(message.text)
                    self.menu = self.menu['reply_buttons'][message.text]['value']
                    await self.methods.send_menu_reply_keyboards(message)

        executor.start_polling(self.dp, skip_updates=True)

    async def customer_start(self, message):
        self.order = [] # order way each customer has been written here
        self.db.insert_into(table_name=variables.user_table_name, data={variables.user_fields[1]: message.chat.id, variables.user_fields[2]: await self.methods.strfdatetime()}, set_unique={variables.user_fields[1]: message.chat.id})
        self.menu = main_menu
        self.message = message
        self.callback_data = await self.methods.send_menu_reply_keyboards(message)

    async def send_order_to_barista(self, order_data, message):
        text = ""
        for key in order_data:
            # text += f"{key}: {order_data[key]}\n"
            text += f"{order_data[key]}\n"

        if self.barista_id:
            for id in self.barista_id:
                await self.bot.send_message(id, text)
                await asyncio.sleep(random.randrange(1, 3))
        else:
            await self.bot.send_message(variables.superadmin_id, f"Поступил заказ на кофе, ни один админ не доступен:\n\n{text}")
        await self.restart_dialog(message, text)

    async def restart_dialog(self, message, text):
        self.menu = restart_dialog
        self.menu['message'] = self.menu['message'].replace('*', f":\n{text}\n")
        self.callback_data = await self.methods.send_menu_reply_keyboards(message)



# if __name__ == "__name__":
#     bot = YourCoffeeBot()
#     bot.bot_handlers()