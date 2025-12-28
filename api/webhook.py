import os
import json
import hashlib
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

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


async def profiles_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка списка профилей"""
    from bot import profile_bot  # Импортируем внутри функции, чтобы избежать проблем с циклическими импортами
    
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
    from bot import profile_bot  # Импортируем внутри функции, чтобы избежать проблем с циклическими импортами
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
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