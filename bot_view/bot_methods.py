from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Methods:

    def __init__(self, main_class):
        self.main_class = main_class

    async def inline_buttons(self, buttons_list:dict):
        buttons = []
        for i in buttons_list:
            buttons.append(InlineKeyboardButton(i, callback_data=buttons_list[i]))
        return buttons


    async def inline_markup(self, buttons:list, row=3):
        buttons = await self.inline_buttons(buttons)
        markup = InlineKeyboardMarkup()
        while len(buttons) > row:
            buttons_row = buttons[0:row]
            buttons = buttons[row:]
            markup.row(*buttons_row)
        return markup

    async def send_message_inline_keyboard(self, buttons, text, *args, **kwargs):
        markup = await self.inline_markup(buttons)
        await self.main_class.bot.send_message(self.main_class.message.chat.id, text, reply_markup=markup)