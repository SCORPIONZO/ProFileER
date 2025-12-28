import os
import json
from telegram.ext import Application, WebhookHandler
from bot import BOT_TOKEN, button_handler, profiles_command, start, help_command

# Получаем токен из переменных окружения
VERCEL_BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем приложение
application = Application.builder().token(VERCEL_BOT_TOKEN).build()

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
        
        # Обновляем объект Update из полученных данных
        update = Update.de_json(body)
        
        # Обрабатываем обновление
        async with application:
            await application.process_update(update)
        
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
    if not VERCEL_BOT_TOKEN:
        print("Ошибка: Необходимо указать токен бота в переменной окружения BOT_TOKEN")
        return

    # Для Vercel мы не запускаем polling, а используем webhook
    print("Бот запущен в режиме webhook для Vercel")


if __name__ == "__main__":
    main()