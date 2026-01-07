import os
import json
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
import hashlib
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Получаем токен из переменных окружения
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN обязательна")

# Создаем приложение
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка сообщения при команде /start"""
    welcome_text = (
        "Добро пожаловать в бота по изучению психологических профилей поведения!\n\n"
        "Это обучающее приложение по профилированию и выявлению обмана.\n\n"
        "Доступные команды:\n"
        "/profiles - Просмотреть список всех психологических профилей\n"
        "/help - Получить справочную информацию\n\n"
        "Выберите интересующий вас профиль из меню ниже:"
    )
    
    keyboard = [[InlineKeyboardButton("Просмотреть профили", callback_data='show_profiles')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка справочной информации при команде /help"""
    help_text = (
        "СПРАВКА:\n\n"
        "Это приложение предназначено для изучения различных типов поведения человека и создания психологических профилей.\n\n"
        
        "КАК ИСПОЛЬЗОВАТЬ:\n"
        "1. Используйте команду /profiles для просмотра всех профилей\n"
        "2. Нажмите на интересующий вас профиль\n"
        "3. Получите подробную информацию о типе поведения\n\n"
        
        "Психологический профиль включает:\n"
        "- Характерные черты\n"
        "- Поведенческие особенности\n"
        "- Тип темперамента\n"
        "- Признаки обмана\n"
        "- Рекомендации по ведению диалога"
    )
    
    await update.message.reply_text(help_text)


class ProfileBot:
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "profiles.json")
        self.profiles = self.load_profiles()
    
    def load_profiles(self):
        """Загрузка профилей из JSON файла"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Пытаемся найти файл в текущей директории
            current_dir_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles.json")
            if os.path.exists(current_dir_file):
                with open(current_dir_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Возвращаем расширенный список примеров профилей
                return [
                    {
                        "name": "Нарциссический тип поведения",
                        "description": "Люди с нарциссическими чертами характера обладают завышенной самооценкой, чрезмерно высоким мнением о себе и отсутствием эмпатии к другим. Они нуждаются в постоянном восхищении и одобрении.",
                        "traits": [
                            "Завышенная самооценка",
                            "Отсутствие эмпатии",
                            "Потребность в восхищении",
                            "Арогантность",
                            "Манипулятивность",
                            "Идеализация себя",
                            "Неосознанное чувство превосходства"
                        ],
                        "behaviors": [
                            "Постоянное стремление быть в центре внимания",
                            "Игнорирование чувств других",
                            "Частое использование других для достижения своих целей",
                            "Отказ признавать ошибки",
                            "Демонстрация превосходства",
                            "Зависть к другим или убежденность в том, что другие завидуют им",
                            "Неуместное поведение в социальных ситуациях"
                        ]
                    },
                    {
                        "name": "Пассивно-агрессивное поведение",
                        "description": "Скрытая форма агрессии, при которой человек косвенно выражает негативные чувства вместо их прямого выражения. Это может проявляться в саботаже, прокрастинации и сарказме.",
                        "traits": [
                            "Косвенное сопротивление",
                            "Прокрастинация",
                            "Сарказм",
                            "Затаивание обиды",
                            "Нежелание сотрудничать",
                            "Отрицание проблем",
                            "Непрямое выражение гнева"
                        ],
                        "behaviors": [
                            "Откладывание выполнения задач",
                            "Саркастические комментарии",
                            "Отказ говорить о проблемах напрямую",
                            "Саботаж",
                            "Жалобы на несправедливость",
                            "Избегание ответственности",
                            "Отрицание личной ответственности за проблемы"
                        ]
                    },
                    {
                        "name": "Антиобщественное расстройство личности",
                        "description": "Хроническое нарушение прав других людей и социальных норм. Люди с этим расстройством часто нарушают закон, лгут, обманывают и не испытывают раскаяния в своих действиях.",
                        "traits": [
                            "Повторяющееся нарушение норм",
                            "Обманчивость",
                            "Импульсивность",
                            "Раздражительность и агрессивность",
                            "Постоянное пренебрежение безопасностью",
                            "Неисполнение обязательств",
                            "Отсутствие раскаяния"
                        ],
                        "behaviors": [
                            "Нарушение закона",
                            "Многократные обманы",
                            "Агрессивное поведение",
                            "Нарушение прав других",
                            "Игнорирование обязанностей",
                            "Пренебрежение безопасностью",
                            "Повторяющиеся проступки"
                        ]
                    }
                ]

    def format_profile(self, profile):
        """Форматирование профиля для вывода в Telegram"""
        text = f"*{profile['name']}*\n\n"
        text += f"{profile['description']}\n\n"
        
        if 'traits' in profile:
            text += "*Характерные черты:*\n"
            text += "• " + "\n• ".join(profile['traits']) + "\n\n"
        
        if 'behaviors' in profile:
            text += "*Поведенческие особенности:*\n"
            text += "• " + "\n• ".join(profile['behaviors']) + "\n\n"
        
        if 'temperament_type' in profile:
            text += f"*Тип темперамента:*\n{profile['temperament_type']}\n\n"
        
        if 'sexual_behavior' in profile:
            text += f"*Сексуальное поведение:*\n{profile['sexual_behavior']}\n\n"
        
        if 'dress_preference' in profile:
            text += f"*Предпочтения в одежде:*\n{profile['dress_preference']}\n\n"
        
        if 'deception_signs' in profile and profile['deception_signs']:
            text += "*Признаки обмана:*\n"
            text += "• " + "\n• ".join(profile['deception_signs']) + "\n\n"
        
        if 'dialog_recommendations' in profile and profile['dialog_recommendations']:
            text += "*Рекомендации по ведению диалога:*\n"
            text += "• " + "\n• ".join(profile['dialog_recommendations']) + "\n\n"
        
        return text.strip()
    
    def get_profile_by_name(self, name):
        """Получение профиля по имени"""
        for profile in self.profiles:
            if profile['name'] == name:
                return profile
        return None
    
    def get_profiles_list(self):
        """Получение списка имен профилей"""
        return [profile['name'] for profile in self.profiles]
    
    def get_deception_indicators_for_profile(self, profile):
        """Получение признаков обмана для конкретного профиля"""
        if 'deception_signs' in profile:
            return profile['deception_signs']
        return []
    
    def get_general_deception_indicators(self):
        """Получение общих признаков обмана"""
        return [
            "Избегание прямого ответа",
            "Противоречивая информация",
            "Несоответствие жестов и слов",
            "Избегание зрительного контакта",
            "Изменение голоса или темпа речи",
            "Агрессивная реакция на вопросы"
        ]
    
    def get_dialog_approaches_for_profile(self, profile):
        """Получение рекомендаций по диалогу для конкретного профиля"""
        if 'dialog_recommendations' in profile:
            return profile['dialog_recommendations']
        return []

# Создаем глобальный экземпляр бота
profile_bot = ProfileBot()

async def profiles_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка списка профилей"""
    keyboard = []
    for profile in profile_bot.profiles:
        # Ограничиваем длину callback_data, используя хэш для длинных имен
        profile_name = profile["name"]
        # Проверяем длину в байтах, а не в символах, так как Telegram проверяет байты
        test_callback = f'profile_{profile_name}'
        if len(test_callback.encode('utf-8')) > 64:  # Убедимся, что callback_data не превышает 64 байта
            profile_hash = hashlib.md5(profile_name.encode()).hexdigest()[:8]
            callback_data = f'profile_{profile_hash}'
        else:
            callback_data = test_callback
        keyboard.append([InlineKeyboardButton(profile["name"], callback_data=callback_data)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите психологический профиль:', reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'show_profiles':
        keyboard = []
        for profile in profile_bot.profiles:
            # Ограничиваем длину callback_data, используя хэш для длинных имен
            profile_key = profile["name"]
            # Проверяем длину в байтах, а не в символах, так как Telegram проверяет байты
            test_callback = f'profile_{profile_key}'
            if len(test_callback.encode('utf-8')) > 64:  # Убедимся, что callback_data не превышает 64 байта
                profile_hash = hashlib.md5(profile_key.encode()).hexdigest()[:8]
                callback_data = f'profile_{profile_hash}'
            else:
                callback_data = test_callback
            keyboard.append([InlineKeyboardButton(profile["name"], callback_data=callback_data)])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await query.edit_message_text(text='Выберите психологический профиль:', reply_markup=reply_markup)
        except Exception:
            # Если не удалось отредактировать сообщение, отправляем новое
            await query.message.reply_text('Выберите психологический профиль:', reply_markup=reply_markup)

    elif query.data.startswith('profile_'):
        # Проверяем, является ли это хэш-идентификатором
        profile_key = query.data[8:]  # Убираем 'profile_' из начала
        
        # Ищем профиль по имени или по хэшу
        profile = None
        for p in profile_bot.profiles:
            # Проверяем оригинальное имя
            test_callback = f'profile_{p["name"]}'
            if p["name"] == profile_key and len(test_callback.encode('utf-8')) <= 64:
                profile = p
                break
            # Проверяем, соответствует ли хэш этому профилю
            elif len(test_callback.encode('utf-8')) > 64:
                expected_hash = hashlib.md5(p["name"].encode()).hexdigest()[:8]
                if expected_hash == profile_key:
                    profile = p
                    break
        
        if profile:
            profile_text = profile_bot.format_profile(profile)
            
            # Добавляем кнопку "Назад"
            keyboard = [[InlineKeyboardButton("Назад к списку профилей", callback_data='show_profiles')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Если текст профиля слишком длинный, разбиваем его на части
            if len(profile_text) > 4096:
                # Разбиваем текст на части по 4000 символов
                parts = []
                for i in range(0, len(profile_text), 4000):
                    parts.append(profile_text[i:i+4000])
                
                # Отправляем все части как отдельные сообщения
                for idx, part in enumerate(parts):
                    if idx == 0:
                        # Для первой части добавляем клавиатуру
                        await query.message.reply_text(text=part, parse_mode='Markdown', reply_markup=reply_markup)
                    else:
                        # Остальные части без клавиатуры
                        await query.message.reply_text(text=part, parse_mode='Markdown')
            else:
                # Если сообщение не длинное, обрабатываем как обычно
                try:
                    # Отправляем информацию о профиле с кнопкой "Назад"
                    await query.edit_message_text(text=profile_text, parse_mode='Markdown', reply_markup=reply_markup)
                except Exception as e:
                    # Если не удалось отредактировать сообщение с клавиатурой, пробуем сначала отредактировать текст
                    try:
                        await query.edit_message_text(text=profile_text, parse_mode='Markdown', reply_markup=None)
                        # Затем отправляем новое сообщение с кнопкой "Назад"
                        await query.message.reply_text(text="Выберите действие:", reply_markup=reply_markup)
                    except Exception:
                        # Если и это не работает, отправляем все в одном новом сообщении
                        await query.message.reply_text(text=profile_text, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            try:
                await query.edit_message_text(text="Профиль не найден.")
            except Exception:
                await query.message.reply_text(text="Профиль не найден.")


# Регистрируем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("profiles", profiles_command))
application.add_handler(CallbackQueryHandler(button_handler))


async def webhook_handler(request):
    """Обработчик вебхука для Vercel"""
    try:
        # Получаем JSON-данные из тела запроса
        body = await request.json()
        
        # Создаем объект Update из полученных данных
        update = Update.de_json(body)
        
        # Обрабатываем обновление
        async with application:
            await application.process_update(update)
        
        # Возвращаем успешный ответ
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"status": "ok"})
        }
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"status": "error", "message": str(e)})
        }


def main():
    """Основная функция для локального тестирования"""
    if not TOKEN:
        print("Ошибка: Необходимо указать токен бота в переменной окружения BOT_TOKEN")
        return

    print("Бот готов к работе с вебхуками на Vercel")


if __name__ == "__main__":
    main()