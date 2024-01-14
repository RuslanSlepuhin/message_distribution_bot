
excel_storage_path = "./media/excel/"
telegram_fields = ['id', 'access_hash', 'username', 'first_name', 'last_name', 'mutual_contact', 'phone']

superuser_start_buttons = {
    "Забрать подписчиков из канала": "get_external_subscribers",
    "Получить свои контакты в Excel": "get_own_contacts",
    "Сделать рассылку": "distribution"
}
get_external_subscribers = "Введи название канала (https://t.me/название канала или просто название канала)"
caption_send_file = "Забирай"
distribution_message = "Закинь сюда Excel с пулом юзеров"
restricted_message = "Интересно, но я не знаю что с этим делать"
distribution_request = "Введи текст для рассылки и отправь его"
distribution_was_success = "Рассылка прошла успешно"
distribution_was_broken = "УПС, что-то пошло не так, обратись к разработчику"
sending_report_file_name = "sending_report"
sending_limit_counter_limit = 20
sending_limit_counter_sleep = 15