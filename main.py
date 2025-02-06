from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


# Вставьте свой токен, полученный от BotFather, сюда
BOT_TOKEN = "7944383872:AAEMrRr0-O2ARA9HzxJzyRrzCyyDP8FahbQ"

# Список участников
players = []
hr_role = None
cards = {}
current_round = 0
finalists = []

# Карты навыков и качеств
skills = ["Воронка продаж", "Стратегия продвижения", "Анализ конкурентов", "Знание графических редакторов", "Подбор цветовой схемы", "оказание первой медицинской помощи", "лечение различных заболеваний", "разработка ПО, сайтов", "знание языков программирования", "написание различных кодов", "знание основ педагогики и психологии", "разработка индивидуального плана обучения", "предотвращение нарушения закона", "знание законов РФ", "знание основ строительного дела и техники безопасности", "выполнение строительно-монтажных работ", "знание иностранного языка", "глубокие культурологические познания различных стран", "проведение расчетов для строительства", "визуализация эскизов и чертежей", "подготовка проектной документации", "составление договоров", "составление исков", "консультирование людей по их правам", "проведение психологических консультаций", "помощь людям в сложных ситуациях", "анализ финансовых показателей", "сбор информации для СМИ", "навыки сценической речи", "умение вживаться в роль", "владение своим телом, мимикой и артикуляцией", "написание статей", "анализ химических реакций", "проведение лабораторный исследований", "консультирование людей по их правам", "оценка состояния конструкции", "способность адаптироваться к любой ситуации", "финансовая грамотность"]
qualities = ["кретивность", "кретивность", "коммуникабельность", "коммуникабельность", "коммуникабельность", "стрессоустойчивость", "усидчивость", "внимательность", "внимательность", "эмпатия", "эмпатия", "ответственность", "ответственность", "исполнительность", "ответственность", "терпеливость", "сдержанность", "честность", "справедливость", "эмпатия"]
negative_skills = ["постоянно опаздывает на работу более, чем на час", "каждый день засыпает на рабочем месте", "обманывает про свое прошлое место работы", "ни разу не пользовался интернетом", "забирает домой вещи с места работы", "избегает людей", "окончил только 9 классов школы", "игровая зависимость", "плохие отношения с руководителем", "очень конфликтный", "не любит работу в команде, необщительный", "неряшливый сотрудник, вечно делает ошибки", "забирает домой вещи с места работы", "медленный, как ленивец из Зверополиса", "социофоб, впадает в панику от общения с клиентами", "гиперактивный, не способен выполнять монотонную работу", "прокрастинатор, всегда находит отговорки", "не выполняет задачи в срок, срывает дедлайны"]
extra_skills = ["отец – директор компании", "прошел курсы у блогера", "окончил МГУ", "прошел стажировку в СберБанке", "отличные рекомендации с прошлого места работы", "3 шаурмичныхна районе", "продает наставничество", "играет в танки с руководителем", "регулярно переводит бабушек через дорогу", "слушает только классическуюмузыку, никаких непристойностей!", "знает всевозможные формулы Excel", "знает много анекдотов из Одноклассников", "каждые выходные будет звать на рыбалку", "не носит носки с сандалиями", "миллион подписчиков в соцсетях", "каждый день приносит пирожки на работу"]

# Карты профессий
professions = ["Программист", "Дизайнер", "Менеджер", "Педагог", "Маркетолог", "Полицейский", "Строитель", "Переводчик", "Архитектор", "Юрист", "Психолог", "Экономист", "Журналист", "Химик", "Предпрениматель", "Актер", "Врач"]


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для игры.\n\nКоманды:\n"
        "/newgame - начать новую игру\n"
        "/show - показать свои навыки, качества и возраст\n"
        "/showdop - показать карту дополнения\n"
        "/podlan - передать карту подлянки\n"
        "/round - объявить текущий раунд (только для HR)\n"
        "/sobes @username1 @username2 - выбрать двух финалистов (только для HR)\n"
        "/stopgame - завершить игру"
    )


# Отправка сообщения с кнопкой "Присоединиться"
async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, hr_role, cards, current_round, finalists

    # Сброс текущих данных
    players = []
    hr_role = None
    cards = {}
    current_round = 0
    finalists = []

    # Сообщение с кнопкой
    keyboard = [
        [InlineKeyboardButton("Присоединиться", callback_data="join_game")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Начинается новая игра! Нажмите на кнопку, чтобы присоединиться.",
        reply_markup=reply_markup
    )


# Обработчик кнопки "Присоединиться"
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players

    query = update.callback_query
    await query.answer()

    user = query.from_user
    user_id = user.id
    user_name = user.first_name

    # Проверяем, если игрок уже в списке
    if any(player["id"] == user_id for player in players):
        return  # Игрок уже присоединился, ничего не делаем

    # Добавляем игрока в список
    players.append({"id": user_id, "name": user_name})

    # Формируем список игроков
    player_names = [player["name"] for player in players]
    player_list = "\n".join(f"- {name}" for name in player_names)

    # Обновляем кнопки: "Присоединиться" и "Начать игру"
    keyboard = [
        [InlineKeyboardButton("Присоединиться", callback_data="join_game")],
        [InlineKeyboardButton("Начать игру", callback_data="start_game")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Обновляем сообщение с добавлением списка игроков
    await query.edit_message_text(
        f"Начинается новая игра! Нажмите на кнопку, чтобы присоединиться.\n\n"
        f"Присоединились:\n{player_list}",
        reply_markup=reply_markup
    )


async def start_game_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players

    query = update.callback_query
    await query.answer()

    if not players:
        await query.edit_message_text("Нельзя начать игру без игроков!")
        return

    # Отправляем сообщение и запускаем раздачу карт
    await query.edit_message_text("Игра начинается! Карты раздаются...")
    await deal(update, context)



# Команда /showall - показывает все свои карты
async def showall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global cards
    user = update.effective_user
    user_id = user.id

    # Проверяем, есть ли карты у игрока
    if user_id not in cards:
        await update.message.reply_text("У вас нет карт. Вы не участвуете в игре.")
        return

    # Извлекаем данные игрока
    player_cards = cards[user_id]
    skills = player_cards.get("skills", [])
    qualities = player_cards.get("qualities", [])
    addition = player_cards.get("extra", None)
    podlan_queue = player_cards.get("podlan_queue", [])
    age = player_cards.get("age", None)
    negative = player_cards.get("negative", [])

    # Формируем текст для ответа с HTML-форматированием
    response = (
        f"<b>Ваши карты:</b>\n\n"
        f"<b>Возраст:</b> <i>{age if age else 'Нет возраста'}</i>\n\n"
        f"<b>Навыки:</b>\n"
        f"<i>- {'</i>, <i>'.join(skills) if skills else 'Нет навыков'}</i>\n\n"
        f"<b>Качества:</b>\n"
        f"<i>- {'</i>, <i>'.join(qualities) if qualities else 'Нет качеств'}</i>\n\n"
        f"<b>Дополнение:</b>\n"
        f"<i>- {addition if addition else 'Нет карты дополнения'}</i>\n\n"
        f"<b>Подлянки:</b>\n"
        f"<i>- {', '.join(negative + podlan_queue) if negative + podlan_queue else 'Нет карт подлянки'}</i>"
    )

    # Отправляем ответ игроку с указанием parse_mode="HTML"
    await update.message.reply_text(response, parse_mode="HTML")


# Генерация возраста
def generate_age():
    return random.choice(range(17, 61, 2))  # Только нечетные числа от 17 до 60


# Команда /deal (раздача карт)
async def deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, hr_role, cards, current_round
    # Проверка, есть ли участники
    if len(players) < 2:
        await update.message.reply_text("Недостаточно игроков для начала игры!")
        return

    # Назначение HR
    if not hr_role:
        hr_role = random.choice(players)
        await context.bot.send_message(
            chat_id=hr_role["id"],
            text="Вы HR! Используйте /round, чтобы начать игру."
        )

    # Раздача карт участникам
    for player in players:
        if player["id"] == hr_role["id"]:
            continue

        player_skills = random.sample(skills, 3)
        player_qualities = random.sample(qualities, 3)
        player_negative = random.choice(negative_skills)
        player_extra = random.choice(extra_skills)
        player_age = generate_age()

        # Инициализация карт для игрока
        cards[player["id"]] = {
            "skills": player_skills,
            "qualities": player_qualities,
            "age": player_age,
            "extra": player_extra,  # Карта дополнения
            "negative": [player_negative],  # Исходная карта подлянки
            "podlan_queue": [],  # Очередь для переданных карт подлянки
            "addition": None  # Дополнительная карта (если требуется)
        }

        # Отправка карт в личные сообщения (с HTML форматированием)
        # Отправка карт в личные сообщения
        await context.bot.send_message(
            chat_id=player["id"],
            text=(
                f"<b>Ваши карты:</b>\n\n"
                f"<b>Возраст:</b> <i>{player_age}</i>\n\n"
                f"<b>Навыки:</b>\n"
                f"<i>- {'</i>, <i>'.join(player_skills)}</i>\n\n"
                f"<b>Качества:</b>\n"
                f"<i>- {'</i>, <i>'.join(player_qualities)}</i>\n\n"
                f"<b>Дополнение:</b>\n"
                f"<i>- {player_extra}</i>\n\n"
                f"<b>Подлянка:</b>\n"
                f"<i>- {player_negative}</i>"
            ),
            parse_mode="HTML"  # Включаем режим HTML
        )

    current_round = 1
    await update.message.reply_text("Карты разосланы участникам! Раунд 1 начался.")


# Команда /round (объявить раунд)
async def round_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_round

    # Проверка, что команду выполняет HR
    if update.effective_user.id != hr_role["id"]:
        await update.message.reply_text("Только HR может объявлять раунды!")
        return

    current_round += 1
    if current_round > 4:
        current_round = 4

    await update.message.reply_text(f"🔔 Раунд {current_round} начался!")


# Команда /show
async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in cards:
        await update.message.reply_text("Вы ещё не получили карты! Используйте команду /deal.")
        return

    user_cards = cards[user.id]
    await update.message.reply_text(
        f"Ваши карты:\n\n"
        f"Возраст: {user_cards['age']}\n\n"
        f"Навыки: {', '.join(user_cards['skills'])}\n"
        f"Качества: {', '.join(user_cards['qualities'])}\n"
    )


# Команда /showdop
async def showdop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in cards:
        await update.message.reply_text("Вы ещё не получили карты! Используйте команду /deal.")
        return

    user_extra = cards[user.id]["extra"]
    await update.message.reply_text(f"🔵 Ваша карта дополнения: {user_extra}")

# Команда /podlan
async def podlan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global cards, players
    user = update.effective_user
    user_id = user.id

    # Проверяем, есть ли у пользователя хотя бы одна карта подлянки
    if user_id not in cards or not cards[user_id].get("negative"):
        await update.message.reply_text("У вас нет карт подлянки для передачи.")
        return

    # Создаем кнопки для каждого игрока (кроме самого себя)
    keyboard = []
    for player in players:
        if player["id"] != user_id:
            keyboard.append([InlineKeyboardButton(player["name"], callback_data=f"podlan_{user_id}_{player['id']}")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопками
    await update.message.reply_text(
        "Кому вы хотите передать карту подлянки?",
        reply_markup=reply_markup
    )


# Обработчик кнопок для /podlan
async def podlan_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global cards
    query = update.callback_query
    await query.answer()

    # Разбираем данные из callback_data
    sender_id, receiver_id = map(int, query.data.split("_")[1:])
    sender_name = next((p["name"] for p in players if p["id"] == sender_id), "Unknown")
    receiver_name = next((p["name"] for p in players if p["id"] == receiver_id), "Unknown")

    # Проверяем, есть ли у отправителя карта подлянки
    if sender_id not in cards or not cards[sender_id].get("negative"):
        await query.edit_message_text("У вас нет карт подлянки для передачи.")
        return

    # Передаём карту
    card_to_give = cards[sender_id]["negative"].pop(0)  # Берём первую карту подлянки у отправителя

    # Добавляем карту подлянки к получателю в очередь
    if receiver_id not in cards:
        cards[receiver_id] = {"skills": [], "qualities": [], "addition": None, "podlan_queue": [], "age": None}

    cards[receiver_id]["podlan_queue"].append(card_to_give)

    # Уведомляем обоих игроков
    await context.bot.send_message(
        chat_id=sender_id,
        text=f"Вы передали карту подлянки '{card_to_give}' игроку {receiver_name}."
    )
    await context.bot.send_message(
        chat_id=receiver_id,
        text=f"Игрок {sender_name} передал вам карту подлянки '{card_to_give}'."
    )

    # Редактируем исходное сообщение
    await query.edit_message_text(f"Вы передали карту подлянки '{card_to_give}' игроку {receiver_name}.")




# Команда /sobes
async def sobes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global hr_role
    # Проверяем, является ли пользователь HR
    user = update.effective_user
    if not hr_role or user.id != hr_role["id"]:
        await update.message.reply_text("Только HR может выбрать номинантов.")
        return

    # Получаем аргументы после команды
    args = context.args
    if not args or len(args) < 2:
        await update.message.reply_text("Укажите двух номинантов. Пример: /sobes палка ручка")
        return

    # Используем первые два аргумента как номинантов
    nominee1 = args[0]
    nominee2 = args[1]

    # Формируем кнопки для выбора победителя
    keyboard = [
        [InlineKeyboardButton(nominee1, callback_data=f"win_{nominee1}")],
        [InlineKeyboardButton(nominee2, callback_data=f"win_{nominee2}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с номинантами
    await update.message.reply_text(
        f"Номинанты на победу:\n1. {nominee1}\n2. {nominee2}\n\nВыберите победителя:",
        reply_markup=reply_markup
    )


# Команда /win
async def win(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global finalists
    if not finalists:
        await update.message.reply_text("Финалисты ещё не выбраны!")
        return

    winner = random.choice(finalists)
    await update.message.reply_text(f"🏆 Победитель: @{winner}!")

# Команда /users - показывает всех участников
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players
    if not players:
        await update.message.reply_text("В игре пока нет участников.")
    else:
        player_names = [player["name"] for player in players]
        await update.message.reply_text(
            "Текущие участники игры:\n" + "\n".join(player_names)
        )


# Команда /stopgame - завершает игру
async def stopgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, hr_role, cards, current_round, finalists
    players = []
    hr_role = None
    cards = {}
    current_round = 0
    finalists = []

    await update.message.reply_text("Игра завершена. Все данные сброшены!")




# Команда /profession - HR получает профессию для игры
async def profession(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global hr_role, professions
    if hr_role is None or hr_role["id"] != update.effective_user.id:
        await update.message.reply_text("Только HR может использовать эту команду!")
        return

    profession = random.choice(professions)
    hr_name = hr_role["name"]

    # Отправляем профессию в общий чат
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"HR {hr_name} выбрал профессию: {profession}"
    )
    # Отправляем HR в личные сообщения
    await context.bot.send_message(
        chat_id=hr_role["id"],
        text=f"Вы выбрали профессию: {profession}"
    )


# Обработчик кнопок для выбора победителя
async def handle_win_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global hr_role
    query = update.callback_query
    await query.answer()

    # Проверяем, что кнопку нажал HR
    user = query.from_user
    if not hr_role or user.id != hr_role["id"]:
        await query.answer("Только HR может выбрать победителя.", show_alert=True)
        return

    # Извлекаем имя победителя из callback_data
    callback_data = query.data
    winner_name = callback_data.split("_")[1]

    # Объявляем победителя
    await query.edit_message_text(f"🏆 Победитель игры: {winner_name}! Поздравляем! 🎉")



# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Основные команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("newgame", new_game))
    app.add_handler(CommandHandler("newgame", new_game))
    app.add_handler(CommandHandler("showall", showall))
    app.add_handler(CallbackQueryHandler(button_callback, pattern="^join_game$"))
    app.add_handler(CallbackQueryHandler(button_callback, pattern="^join_game$"))
    app.add_handler(CallbackQueryHandler(start_game_callback, pattern="^start_game$"))
    app.add_handler(CommandHandler("deal", deal))
    app.add_handler(CallbackQueryHandler(podlan_callback, pattern=r"^podlan_\d+_\d+$"))
    # Дополнительные команды
    app.add_handler(CommandHandler("show", show))
    app.add_handler(CommandHandler("showdop", showdop))
    app.add_handler(CommandHandler("podlan", podlan))
    app.add_handler(CommandHandler("round", round_command))
    app.add_handler(CommandHandler("sobes", sobes))
    app.add_handler(CommandHandler("win", win))
    app.add_handler(CommandHandler("users", users))
    app.add_handler(CommandHandler("stopgame", stopgame))
    app.add_handler(CommandHandler("showall", showall))
    app.add_handler(CommandHandler("profession", profession))
    app.add_handler(CallbackQueryHandler(handle_win_callback, pattern=r"^win_"))

    # Запуск бота
    app.run_polling()

