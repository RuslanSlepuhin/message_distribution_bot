import urllib
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_view.teleth_bot import TelethBot
from variables import variables
import pandas as pd
from helper.file_operations import write_to_excel

class Methods:

    def __init__(self, main_class):
        self.main_class = main_class

    async def inline_buttons(self, buttons_list:dict):
        buttons = []
        for i in buttons_list:
            buttons.append(InlineKeyboardButton(i, callback_data=buttons_list[i]))
        return buttons

    async def inline_markup(self, buttons:dict, **kwargs):
        callbacks = list(buttons.values())
        row = 3 if not kwargs.get('row') or not kwargs['row'] else kwargs['row']
        buttons = await self.inline_buttons(buttons)
        markup = InlineKeyboardMarkup()
        while len(buttons) > row:
            buttons_row = buttons[0:row]
            buttons = buttons[row:]
            markup.row(*buttons_row)
        markup.row(*buttons)
        return markup, callbacks

    async def send_message_inline_keyboard(self, message, buttons, text, **kwargs):
        row = kwargs['row'] if kwargs.get('row') else None
        markup, callbacks = await self.inline_markup(buttons, row=row)
        await self.main_class.bot.send_message(message.chat.id, text, reply_markup=markup)
        return callbacks

    async def get_external_subscribers(self, message, channel):
        teleth = TelethBot()
        file_path, error = await teleth.get_subscribers(channel_name=channel)
        if not error:
            print(file_path)
            await self.send_file(message, file_path)
        else:
            await self.main_class.bot.send_message(message.chat.id, f"Sorry, I can't do it cause:\n{str(error)}")

    async def send_file(self, message, file_path, caption=variables.caption_send_file):
        with open(file_path, 'rb') as file:
            try:
                await self.main_class.bot.send_document(message.chat.id, file, caption=caption)
            except Exception as ex:
                await self.main_class.bot.send_message(message.chat.id, ex)

    async def get_own_contacts(self, message):
        teleth = TelethBot()
        file_path = await teleth.get_my_contacts()
        print(file_path)
        await self.send_file(message, file_path)

    async def receive_excel(self, message):
        document_id = message.document.file_id
        file_info = await self.main_class.bot.get_file(document_id)
        fi = file_info.file_path
        file_name = message.document.file_name
        urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{self.main_class.token}/{fi}', f'{variables.excel_storage_path}{file_name}')
        return await self.parse_excel(file_name)

    async def parse_excel(self, file_name):
        fields = variables.telegram_fields
        excel_data_df = pd.read_excel(variables.excel_storage_path + file_name, sheet_name='Sheet1')
        excel_dict = {}
        for field in fields:
            excel_dict[field] = excel_data_df[field].tolist()
        return excel_dict

    async def distribution(self, id_list:list, message_text:str):
        teleth = TelethBot()
        response, report_dict = await teleth.pull_message_to_users(id_list, message_text)
        await self.prepare_report(report_dict)
        return response

    async def prepare_report(self, report_dict):
        if len(report_dict['id']) > len(report_dict['sending_report']):
            for i in range(0, len(report_dict['id'])-len(report_dict['sending_report'])):
                report_dict['sending_report'].append(False)
        file_path = await write_to_excel(report_dict, variables.sending_report_file_name)
        await self.send_file(self.main_class.message, file_path, caption="Отчет об отправке сообщений (столбец sending_report)")






