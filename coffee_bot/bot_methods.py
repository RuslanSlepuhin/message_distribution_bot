from datetime import datetime
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from coffee_bot import variables
import pandas as pd

class Methods:
    def __init__(self, main):
        self.main = main

    async def send_menu_reply_keyboards(self, message, **kwargs):
        buttons = []
        callback_data = []
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for i in self.main.menu['reply_buttons'].keys():
            buttons.append(KeyboardButton(i))
            callback_data.append(self.main.menu['reply_buttons'][i]['callback'])
        markup.add(*buttons)
        if self.main.menu['row'] == 0 or not self.main.menu['reply_buttons']:
            await self.main.bot.send_message(chat_id=message.chat.id, text=self.main.menu['message'], reply_markup=ReplyKeyboardRemove())
            await self.main.PhoneNumberState.phone_number.set()
        else:
            await self.main.bot.send_message(chat_id=message.chat.id, text=self.main.menu['message'], reply_markup=markup)
        return callback_data

    def get_barista_id_list(self, responses):
        return [i[1] for i in responses]

    async def strfdatetime(self):
        return datetime.now().strftime("%y-%m-%d %H:%M")

    async def send_photo(self, path, message):
        with open(path, "rb") as file:
            await self.main.bot.send_photo(message.chat.id, file)

    async def get_users(self, message):
        excel_data = {}
        for i in variables.user_fields:
            excel_data[i] = []
        responses = self.main.db.select_from(variables.user_table_name, data=None, select=True)
        if responses:
            for response in responses:
                for i in range(0, len(variables.user_fields)):
                    data = response[i] if response[i] else "-"
                    excel_data[variables.user_fields[i]].append(data)
        full_path = await self.write_to_excel(excel_data)
        await self.send_file(full_path, message)


    async def write_to_excel(self, excel_data, file_name=variables.excel_storage_path, path=variables.media_path):
        df = pd.DataFrame(excel_data)
        file_name = "data.xlsx" if not file_name else file_name
        file_full_path = path + file_name
        df.to_excel(file_full_path, sheet_name='Sheet1')
        print(f'\nExcel was writting')
        return file_full_path

    async def send_file(self, path, message):
        with open(path, "rb") as file:
            await self.main.bot.send_document(message.chat.id, file, caption="Отчет по пользователям")
