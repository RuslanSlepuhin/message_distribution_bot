import pandas as pd
import configparser
from variables import variables
from telethon import functions
from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

config = configparser.ConfigParser()
config.read(".\settings\config.ini")

api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

class TelethBot:

    def init_bot(self):
        self.client = TelegramClient(username, int(api_id), api_hash)
        with self.client:
            self.client.loop.run_until_complete(self.create_new_session())

    async def create_new_session(self):
        await self.client.connect()
        await self.get_subscribers("https://t.me/salon_director")
        # await self.get_my_contacts()
        # await self.pull_message_to_users(["g", "g"], "Test Text, Sorry)")
        # return self.client


    async def get_subscribers(self, channel_name="https://t.me/Rabkova_EV"):
        channel = await self.client.get_entity(channel_name)
        filter_user = ChannelParticipantsSearch('')
        offset_user = 0  # номер участника, с которого начинается считывание
        limit_user = 100  # максимальное число записей, передаваемых за один раз
        pass
        participants = []
        participants_list = []
        while True:
            participants = await self.client(GetParticipantsRequest(
                channel, filter_user, offset_user, limit_user, hash=0))
            offset_user += limit_user
            print(offset_user)
            if not participants.users:
                break
            participants_list.extend(participants.users)
            pass

        await self.prepare_excel_dict_data(participants_list, variables.telegram_fields, channel_name.split("/")[-1])

    async def get_my_contacts(self) -> None:
        result = await self.client(functions.contacts.GetContactsRequest(
            hash=0  # Using 0 for hash will fetch all contacts
        ))
        await self.prepare_excel_dict_data(result.users, variables.telegram_fields, "My_contacts")

    async def prepare_excel_dict_data(self, participants_list, fields, file_name) -> None:
        user_excel_data = {}
        for user in participants_list:
            for field in fields:
                if field not in user_excel_data:
                    user_excel_data[field] = []
                # print(participants_list.index(user), field)
                match field:
                    case 'id': user_excel_data[field].append(user.id)
                    case 'access_hash': user_excel_data[field].append(user.access_hash)
                    case 'username': user_excel_data[field].append(user.username)
                    case 'first_name': user_excel_data[field].append(user.first_name)
                    case 'last_name': user_excel_data[field].append(user.last_name)
                    case 'mutual_contact': user_excel_data[field].append(user.mutual_contact)
                    case 'phone': user_excel_data[field].append(user.phone)
                pass
            pass
            # if participants_list.index(user) == 10:
            #     break
        await self.write_to_excel(user_excel_data, file_name)

    async def write_to_excel(self, user_excel_data, file_name, path="media/excel/") -> None:
        df = pd.DataFrame(
            {
                'id': user_excel_data['id'],
                'access_hash': user_excel_data['access_hash'],
                'username': user_excel_data['username'],
                'first_name': user_excel_data['first_name'],
                'last_name': user_excel_data['last_name'],
                'mutual_contact': user_excel_data['mutual_contact'],
                'phone': user_excel_data['phone'],
            }
        )


        file_name = "data.xlsx" if not file_name else file_name + ".xlsx"
        df.to_excel(path + file_name, sheet_name='Sheet1')
        print(f'\nExcel was writting')
        await self.pull_message_to_users(user_excel_data, "test text, sorry)")

    async def pull_message_to_users(self, user_excel_data:list, message_text:str) -> None:
        # for user_id in user_excel_data['id']:
        #     await self.client.send_message(user_id, message_text)
        #     pass
        # await self.client.send_message(5502797471, message_text)
        pass



