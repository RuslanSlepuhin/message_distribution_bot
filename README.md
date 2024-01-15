# Message Distribution Bot
What it does:
1. Receives followers from external channels in Excel file
2. Receives my contacts in Excel file
3. Sends messages to telegram users from received file from 1 and 2 points 

Quick Start:
1. git clone url
2. cd message_distribution_bot
3. python venv app-env (create the virtual environment)
4. pip install -r requirements.txt (install lybraries)
5. app-env/scripts/activate (Windows); source app-env/bin/activate (Ubuntu)
6. mkdir media -> cd media -> mkdir excel -> cd .. (make directory for Excel files storage)
7. python -m main_start (run the app)

Stack:
1. Telethon
2. Aiogram
3. Pandas
4. 