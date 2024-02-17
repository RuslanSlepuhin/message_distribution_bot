
superadmin_id = 5884559465
database_location_path = "./coffee_bot/database/coffee.db"

# ------------ BARISTA TABLE ----------------
barista_table_name = 'barista'
barista_sql_create = """CREATE TABLE IF NOT EXISTS barista (id INTEGER PRIMARY KEY, telegram_user_id INTEGER NOT NULL UNIQUE);"""
barista_fields = ['id', 'telegram_user_id']
add_barista_command = 'barista'
remove_barista_command = 'remove_barista'

start_barista_message = "Вы бариста, ожидайте поступление онлайн заказов, они буду поступать в этот бот. Более подробную инструкцию можно прочитать в разделе /help"
remove_barista_message = "Вы больше не бариста, вы не сможете принимать онлайн заказы, можете использовать этот бот для заказа кофе в роли посетителя кофейни 'Твой кофе'"

# ------------ USER TABLE -----------------
user_table_name = 'user'
user_sql_create = """CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, telegram_user_id INTEGER NOT NULL, start_date_time VARCHAR(50), orders VARCHAR(255), order_date_time VARCHAR(50), phone_number VARCHAR(30), free_message VARCHAR(300));"""
user_fields = ['id', 'telegram_user_id', 'start_date_time', 'orders', 'order_date_time', 'phone_number', 'free_message']

media_path = "./coffee_bot/media/"
menu_jpg_path = "Меню Coffee You.jpg"
excel_storage_path = "users_report.xlsx"

admin_help = "Вы видите эту инструкцию, потому, что вы - суперадмин. Другим пользователям бота эта информация недоступена\n\n" \
             "Инструкция по боту:\n" \
             "/barista - телефон пользователя, который выполнил эту команду становится телефоном, " \
             "на который приходят онлайн заказы. Сервис по заказу кофе с этого телефона недоступен\n" \
             "/remove_barista - возвращает пользователя в статус обычного пользователя услуг кофейни\n" \
             "Если бариста никто не назначен, онлайн заказы приходят суперадмину\n" \
             "/get_users - получить EXCEL с пользователями, которые что-либо уже заказывали (в базе хранится последний из заказов), либо заходили в бот. Пулл этих пользователей можно включать в тематическую рассылку"
user_help = "Вы можете сделать онлайн заказ на напитки из кофейни COFFEE YOU\nНажмите /start и следуйте подсказкам"