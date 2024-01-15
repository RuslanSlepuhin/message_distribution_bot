# Message Distribution Bot
What it does:
1. Receives followers from external channels in Excel file
2. Receives my contacts in Excel file
3. Sends messages to telegram users from received file from 1 and 2 points 

Quick Start:
1. git clone url
2. cd message_distribution_bot
3. python venv app-env (create the virtual environment)
4. app-env/scripts/activate (Windows); source app-env/bin/activate (Ubuntu)
5. pip install -r requirements.txt (install lybraries)
6. mkdir media -> cd media -> mkdir excel -> cd .. (make directory for Excel files storage)
7. go to https://t.me/BotFather and create the bot, copy the token for future
8. go to https://my.telegram.org/ to get your telegram api_id and api_hash fo future
9. mkdir settings and create config.ini
>[TelegramProduction] \
>api_id = 'your api_id' \
>api_hash = 'your api_hash' \
>username = 'username' -> The value doesn't matter \
> \
>[Bot] \
>token = "your bot token" \
> \
> [Admins] \
>superuser = "telegram_id", "telegram_id", ...
>
9. python -m main_start (run the app)

Enjoy)

Stack:
1. Telethon
2. Aiogram
3. Pandas