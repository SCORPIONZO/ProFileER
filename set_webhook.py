import os
import sys
import asyncio
import httpx

async def set_webhook():
    """Устанавливаем вебхук для бота на Vercel"""
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        print("Ошибка: Не установлен BOT_TOKEN")
        return

    # URL для установки вебхука (замените YOUR_VERCEL_PROJECT_URL на ваш URL)
    vercel_project_url = input("Введите URL вашего проекта на Vercel (например, https://your-project.vercel.app): ").strip()
    if not vercel_project_url:
        print("URL проекта не может быть пустым")
        return

    webhook_url = f"{vercel_project_url}/webhook"
    
    api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    payload = {
        "url": webhook_url
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, json=payload)
        result = response.json()

    if result.get("ok"):
        print(f"Вебхук успешно установлен на: {webhook_url}")
        print("Бот готов к работе с вебхуками!")
    else:
        print(f"Ошибка при установке вебхука: {result.get('description')}")


if __name__ == "__main__":
    asyncio.run(set_webhook())