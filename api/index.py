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

# Импортируем функции из основного бота
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
        self.data_file = "profiles.json"
        self.profiles = self.load_profiles()
    
    def load_profiles(self):
        """Загрузка профилей из JSON файла"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Файл {self.data_file} не найден, создаем пустой список")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка чтения {self.data_file}, создаем пустой список")
            return []
    
    def format_profile(self, profile):
        """Форматирование профиля для отправки в Telegram"""
        profile_text = f"*{profile['name']}*\n\n"
        profile_text += f"_{profile['description']}_\n\n"
        
        profile_text += "*ХАРАКТЕРНЫЕ ЧЕРТЫ:*\n"
        for trait in profile["traits"]:
            profile_text += f"• {trait}\n"
        
        profile_text += "\n*ПОВЕДЕНЧЕСКИЕ ОСОБЕННОСТИ:*\n"
        for behavior in profile["behaviors"]:
            profile_text += f"• {behavior}\n"
        
        # Добавляем дополнительные поля если они существуют
        if "temperament" in profile:
            profile_text += "\n*ТИП ТЕМПЕРАМЕНТА:*\n"
            for temperament in profile.get("temperament", ["Информация отсутствует"]):
                profile_text += f"• {temperament}\n"
        
        if "sexual_behavior" in profile:
            profile_text += "\n*СЕКСУАЛЬНОЕ ПОВЕДЕНИЕ:*\n"
            for behavior in profile.get("sexual_behavior", ["Информация отсутствует"]):
                profile_text += f"• {behavior}\n"
        
        if "clothing_preferences" in profile:
            profile_text += "\n*ПРЕДПОЧТЕНИЯ В ОДЕЖДЕ:*\n"
            for clothing in profile.get("clothing_preferences", ["Информация отсутствует"]):
                profile_text += f"• {clothing}\n"
        
        # Добавляем анализ обмана
        profile_text += "\n*АНАЛИЗ ПОВЕДЕНИЯ НА ПРЕДМЕТ ОБМАНА:*\n"
        deception_indicators = self.get_deception_indicators_for_profile(profile)
        if deception_indicators:
            profile_text += f"Признаки обмана для профиля '{profile['name']}':\n"
            for indicator in deception_indicators:
                profile_text += f"• {indicator}\n"
        else:
            profile_text += f"Профиль '{profile['name']}' не содержит специфических признаков обмана.\n"
        
        # Добавляем общие признаки обмана
        profile_text += "\n*ОБЩИЕ ПРИЗНАКИ ОБМАНА В ПОВЕДЕНИИ:*\n"
        general_indicators = self.get_general_deception_indicators()
        for indicator in general_indicators:
            profile_text += f"• {indicator}\n"
        
        # Добавляем рекомендации по диалогу
        profile_text += "\n*ВЕДЕНИЕ ДИАЛОГА С ТИПОМ ЛИЧНОСТИ:*\n"
        dialog_approaches = self.get_dialog_approaches_for_profile(profile)
        for approach in dialog_approaches:
            profile_text += f"• {approach}\n"
        
        return profile_text
    
    def get_general_deception_indicators(self):
        """Получение общих признаков обмана"""
        return [
            "Изменение жестов и мимики (увеличение или уменьшение)",
            "Контрольные движения: прикосновения к лицу, уху, горлу",
            "Непривычное поведение, нехарактерное для человека",
            "Избегание зрительного контакта или наоборот чезмерное внимание",
            "Физиологические признаки стресса: потливость, дрожь, покраснение"
        ]
    
    def get_deception_indicators_for_profile(self, profile):
        """Получение специфических признаков обмана для профиля"""
        # В реальной реализации это будет зависеть от конкретного профиля
        # Пока возвращаем пустой список
        return []
    
    def get_dialog_approaches_for_profile(self, profile):
        """Получение рекомендаций по диалогу для конкретного профиля"""
        name_lower = profile["name"].lower()
        approaches = [
            "Создайте комфортную обстановку для диалога",
            "Используйте соответствующий тон общения",
            "Учитывайте особенности поведения профиля"
        ]
        
        return approaches


async def profiles_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка списка профилей"""
    profile_bot = ProfileBot()  # Создаем экземпляр бота
    
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
    profile_bot = ProfileBot()  # Создаем экземпляр бота
    
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
            
            # Проверяем длину сообщения и разбиваем на части при необходимости
            if len(profile_text) > 4096:  # Лимит Telegram для текста сообщения
                parts = []
                current_part = ""
                for line in profile_text.split("\n"):
                    if len(current_part + line + "\n") <= 4000:  # Оставляем запас на форматирование
                        current_part += line + "\n"
                    else:
                        if current_part:  # Если текущая часть не пустая
                            parts.append(current_part)
                        current_part = line + "\n"
                
                if current_part.strip():  # Добавляем последнюю часть, если она не пустая
                    parts.append(current_part)
                
                try:
                    # Отправляем первую часть с клавиатурой
                    await query.edit_message_text(text=parts[0], parse_mode='Markdown', reply_markup=reply_markup)
                    
                    # Отправляем оставшиеся части как новые сообщения
                    for part in parts[1:]:
                        await query.message.reply_text(text=part, parse_mode='Markdown')
                except Exception:
                    # Если не удалось отредактировать сообщение, отправляем все части как новые сообщения
                    for part in parts:
                        await query.message.reply_text(text=part, parse_mode='Markdown')
                    
                    # Отправляем сообщение с клавиатурой отдельно
                    await query.message.reply_text(text="Выберите действие:", reply_markup=reply_markup)
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


async def handle(request):
    """Основная функция обработки запросов для Vercel"""
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