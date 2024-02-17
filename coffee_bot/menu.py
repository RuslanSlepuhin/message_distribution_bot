def after_volume(object):
    match object:
        case "capuccino": return []

finish = {
    "message": "Напишите, что заберёте напиток у бара либо укажите свой номер телефона и имя, а мы узнаем, куда нужно принести ваш напиток! "
               "[напишите одним сообщением]:",
    "reply_buttons": {},
    'row': 1,
}

# -------------- CLASSIC MENU ----------------
milk = {
    "message": "Выберите молоко:",
    "reply_buttons": {
        "Обычное": {"callback": "normal_milk", "value": finish},
        "Кокосовое": {"callback": "coconut_milk", "value": finish},
        "Банановое": {"callback": "banana_milk", "value": finish},
        "Миндальное": {"callback": "almond_milk", "value": finish},
        "Овсяное": {"callback": "oat_milk", "value": finish},
        "Назад": {"callback": "cancel", "value": None},
    },
    'row': 1,
}

capuccino_volume = {
    "message": "Выберите объем: ",
    "reply_buttons": {
        "200 мл": {"callback": "200", "value": milk},
        "300 мл": {"callback": "300", "value": milk},
        "500 мл": {"callback": "500", "value": milk},
        "Назад": {"callback": "cancel", "value": None},
    },
    'row': 1,
}
latte_volume = {
    "message": "Выберите объем: ",
    "reply_buttons": {
        "300 мл": {"callback": "300", "value": milk},
        "500 мл": {"callback": "500", "value": milk},
        "Назад": {"callback": "cancel", "value": None},
    },
    'row': 1,
}
flat_white_volume = {
    "message": "Выберите объем: ",
    "reply_buttons": {
        "200 мл": {"callback": "200", "value": finish},
        "300 мл": {"callback": "300", "value": finish},
        "Назад": {"callback": "cancel", "value": finish},
    },
    'row': 1,
}
american_volume = {
    "message": "Выберите объем: ",
    "reply_buttons": {
        "200 мл": {"callback": "200", "value": finish},
        "300 мл": {"callback": "300", "value": finish},
        "500 мл": {"callback": "500", "value": finish},
        "Назад": {"callback": "cancel", "value": None},
    },
    'row': 1,
}
espresso_volume = None
moccachino_volume = latte_volume
cocoa_with_marshmallow_volume = latte_volume
cocoa_volume = cocoa_with_marshmallow_volume
masala_volume = {
    "message": "Выберите объем: ",
    "reply_buttons": {
        "300 мл": {"callback": "300", "value": finish},
        "500 мл": {"callback": "500", "value": finish},
        "Назад": {"callback": "cancel", "value": None},
    },
    'row': 1,
}
matcha_volume = masala_volume

raf_volume = latte_volume

fresh_juice_volume = {
    "message": "Выберите объем: ",
    "reply_buttons": {
        "300 мл": {"callback": "300", "value": milk},
        "500 мл": {"callback": "500", "value": milk},
        "Назад": {"callback": "cancel", "value": None},
    },
    'row': 1,
}


# ------------------- TEA ------------------


matcha_and_masala = {
    "message": "Выберите напиток: ",
    "reply_buttons": {
        "Матча": {"callback": "matcha", "value": matcha_volume},
        "Масала": {"callback": "masala", "value": masala_volume},
        "Назад": {"callback": "cancel", "value": None},
    },
    'row': 1,
}

tea_volume = {
    "message": "Выберите объем: ",
    "reply_buttons": {
        "400мл": {"callback": "400", "value": finish},
        "600мл (чайник)": {"callback": "600", "value": finish},
        "Назад": {"callback": "cancel", "value": None},
    },
    'row': 1,
}

tea_values = {
    "message": "Выберите чай: ",
    "reply_buttons": {
        "Чёрный": {"callback": "tea_black", "value": tea_volume},
        "Ройбуш": {"callback": "tea_raspberries_mint", "value": tea_volume},
        "Молочный Улун": {"callback": "", "value": tea_volume},
        "Пуэр": {"callback": "", "value": tea_volume},
        "Фруктовый": {"callback": "", "value": tea_volume},
        "Малина-Мята": {"callback": "", "value": tea_volume},
        "Гречишный": {"callback": "", "value": tea_volume},
        "Назад": {"callback": "cancel", "value": None},
    },
    'row': 1,
}
# ------------------- FRESH JUICE -----------------


# ------------------- RAF ---------------------
raf = {
    "message": "Выберите напиток: ",
    "reply_buttons": {
        "Ванильный": {"callback": "raf_vanilla", "value": raf_volume},
        "Карамельный": {"callback": "raf_caramel", "value": raf_volume},
        "Кокосовый": {"callback": "raf_raf_coconut", "value": raf_volume},
        "Лавандовый": {"callback": "raf_lavender", "value": raf_volume},
        "Роза": {"callback": "raf_rose", "value": raf_volume},
        "Халва": {"callback": "raf_halva", "value": raf_volume},
        "Апельсин": {"callback": "raf_orange", "value": raf_volume},
        "Назад": {"callback": "cancel", "value": None},
    },
    'row': 1,
}

tea = {
    "message": "Выберите напиток: ",
    "reply_buttons": {
         "Чай": {"callback": "tea", "value": tea_values},
         "Матча и Масала": {"callback": "matcha_and_masala", "value": matcha_and_masala},
         "Назад": {"callback": "back", "value": None},
     },
     'row': 1,
}

fresh_juice = {
    "message": "Выберите напиток: ",
    "reply_buttons": {
        "Апельсиновый": {"callback": "juice_orange", "value": fresh_juice_volume},
        "Грейпфрутовый": {"callback": "juice_grapefruit", "value": fresh_juice_volume},
        "Яблочный": {"callback": "juice_apple", "value": fresh_juice_volume},
        "Морковный": {"callback": "juice_carrot", "value": fresh_juice_volume},
        "Назад": {"callback": "cancel", "value": None},
    },
    'row': 1,
}

classic_menu = {
    "message": "Выберите напиток: ",
    "reply_buttons": {
        "Капучино": {"callback": "capuccino", "value": capuccino_volume},
        "Латте": {"callback": "latte", "value": latte_volume},
        "Флэт уайт": {"callback": "flat_white", "value": flat_white_volume},
        "Американо": {"callback": "american", "value": american_volume},
        "Эспрессо": {"callback": "espresso", "value": finish},
        "Моккачино": {"callback": "moccachino", "value": moccachino_volume},
        "Какао с маршмеллоу": {"callback": "cocoa_with_marshmallow", "value": cocoa_with_marshmallow_volume},
        "Какао": {"callback": "cocoa", "value": cocoa_volume},
        "Назад": {"callback": "back", "value": None}
        },
    'row': 2,
}

main_menu = {
    "message": "☕️ Через этого бота вы можете заказать себе кофе из кофейни Your Coffee!",
    "reply_buttons": {
        "Классическое меню": {"callback": "classic_menu", "value": classic_menu},
        "Раф": {"callback": "raf", "value": raf},
        "Чай": {"callback": "tea", "value": tea},
        "Свежевыжатый сок": {"callback": "fresh_juice", "value": fresh_juice},
        "Показать меню": {"callback": "show_menu", "value": None},
        "Заказать одним сообщением": {"callback": "order_by_message", "value": None},
    },
    'row': 2,
}

restart_dialog = {
    "message": "Ваш заказ отправлен бармену* Вы можете разместить второй заказ",
    "reply_buttons": {
        "Заказать еще": {"callback": "order_more", "value": None},
    },
    'row': 1,
}