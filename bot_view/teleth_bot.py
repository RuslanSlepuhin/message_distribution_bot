import asyncio
import random
import re
from helper.file_operations import write_to_excel
import configparser
from variables import variables
from telethon import functions
from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

config = configparser.ConfigParser()
config.read("./settings/config.ini")

key_telegram = variables.key_telegram_config
api_id = config[key_telegram]['api_id']
api_hash = config[key_telegram]['api_hash']
username = config[key_telegram]['username']

class TelethBot:

    def init_bot(self):
        self.client = TelegramClient(username, int(api_id), api_hash)
        self.client.start()
        pass

    # def init_bot(self):
    #     self.client = TelegramClient(username, int(api_id), api_hash)
    #     with self.client:
    #         self.client.loop.run_until_complete(self.create_new_session())

    async def create_new_session(self):
        try:
            await self.client.start()
        except ConnectionError:
            print('Failed to establish a connection with Telegram')
        print("telethon telegram account was started")
        await self.client.disconnect()

    async def get_subscribers(self, channel_name):
        self.client = TelegramClient(username, int(api_id), api_hash)
        await self.client.connect()

        channel = await self.client.get_entity(channel_name)
        filter_user = ChannelParticipantsSearch('')
        offset_user = 0
        limit_user = 100
        participants_list = []
        while True:
            try:
                participants = await self.client(GetParticipantsRequest(channel, filter_user, offset_user, limit_user, hash=0))
                offset_user += limit_user
                print(offset_user)
                if not participants.users:
                    break
                participants_list.extend(participants.users)
            except Exception as ex:
                return '', str(ex)
        file_full_path = await self.prepare_excel_dict_data(participants_list, variables.telegram_fields, channel_name.split("/")[-1])
        await self.client.disconnect()
        return file_full_path, None

    async def get_my_contacts(self) -> None:
        self.client = TelegramClient(username, int(api_id), api_hash)
        await self.client.connect()

        result = await self.client(functions.contacts.GetContactsRequest(
            hash=0  # Using 0 for hash will fetch all contacts
        ))
        file_full_path = await self.prepare_excel_dict_data(result.users, variables.telegram_fields, "My_contacts")
        await self.client.disconnect()
        return file_full_path

    async def prepare_excel_dict_data(self, participants_list, fields, file_name) -> None:
        user_excel_data = {}
        for user in participants_list:
            for field in fields:
                if field not in user_excel_data:
                    user_excel_data[field] = []
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
        return await write_to_excel(user_excel_data, file_name)

    async def pull_message_to_users(self, user_excel_data, message_text:str) -> [bool, dict]:
        self.client = TelegramClient(username, int(api_id), api_hash)
        await self.client.connect()
        user_excel_data['sending_report'] = []
        user_excel_data_id = user_excel_data['id'] if type(user_excel_data) is dict and user_excel_data.get('id') else user_excel_data
        sending_limit_counter = 0
        for user in user_excel_data_id:
            try:
                await self.client.send_message(int(user), message_text)
                await asyncio.sleep(random.randrange(1, 4))
                user_excel_data['sending_report'].append(True)
                sending_limit_counter += 1
                print("user_id ", user)
            except Exception as ex:
                print("message not was sent to user_id ", user)
                if "flood control" in str(ex):
                    print('flood control', ex)
                    sleep_seconds = re.findall(r"[0-9]+", str(ex))[0] + 10
                    print('sleep_seconds', sleep_seconds)
                    await asyncio.sleep(sleep_seconds)
                user_excel_data['sending_report'].append(False)
            if sending_limit_counter > variables.sending_limit_counter_limit:
                await asyncio.sleep(variables.sending_limit_counter_sleep)
                sending_limit_counter = 0

        await self.client.disconnect()
        return True, user_excel_data

if __name__ == '__main__':
    t = TelethBot()
    t.init_bot()

