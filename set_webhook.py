import os
import sys
import asyncio
import httpx

async def set_webhook():
    """Устанавливаем вебхук для бота на Vercel"""
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        print("Ошибка: Не установлен BOT_TOKEN")
        print("Установите переменную окружения BOT_TOKEN:")
        print("export BOT_TOKEN='ваш_токен_бота'")
        return

    # URL для установки вебхука (замените YOUR_VERCEL_PROJECT_URL на ваш URL)
    vercel_project_url = input("Введите URL вашего проекта на Vercel (например, https://your-project.vercel.app): ").strip()
    if not vercel_project_url:
        print("URL проекта не может быть пустым")
        return

    # Убедимся, что URL начинается с https://
    if not vercel_project_url.startswith('http'):
        vercel_project_url = 'https://' + vercel_project_url

    # Убираем слэш в конце, если он есть
    if vercel_project_url.endswith('/'):
        vercel_project_url = vercel_project_url.rstrip('/')

    webhook_url = f"{vercel_project_url}/api"

    api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    payload = {
        "url": webhook_url
    }

    print(f"Устанавливаю вебхук на: {webhook_url}")

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, json=payload)
        result = response.json()

    if result.get("ok"):
        print(f"✅ Вебхук успешно установлен на: {webhook_url}")
        print("Бот готов к работе с вебхуками!")
        print("\n💡 Если бот не отвечает, проверьте:")
        print("- Правильно ли задан URL (должен быть формата https://your-project.vercel.app)")
        print("- Установлен ли BOT_TOKEN в настройках Vercel")
        print("- Есть ли доступ к интернету у сервера Vercel")
    else:
        print(f"❌ Ошибка при установке вебхука: {result.get('description')}")


if __name__ == "__main__":
    asyncio.run(set_webhook())