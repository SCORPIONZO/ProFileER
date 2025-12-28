#!/usr/bin/env python3
"""
Скрипт для настройки Telegram-бота
"""

import os
import sys
from pathlib import Path

def setup_bot_token():
    """Настройка токена Telegram-бота"""
    print("Настройка Telegram-бота для ProFileER")
    print("="*50)
    
    print("\033[91mВАЖНО: Если вы уже опубликовали токен где-либо (включая использование")
    print("в чатах с ИИ), вы ДОЛЖНЫ создать нового бота или сбросить токен старого,")
    print("так как опубликованный токен считается скомпрометированным.\033[0m")
    
    # Запрашиваем токен у пользователя
    token = input("Введите токен вашего Telegram-бота (получить у @BotFather): ").strip()
    
    if not token:
        print("Токен не может быть пустым!")
        sys.exit(1)
    
    # Проверяем формат токена (обычно состоит из цифр и букв, разделенных двоеточием)
    if ':' not in token:
        print("Вероятно, токен введен неправильно (должен содержать двоеточие)")
        response = input("Продолжить с этим токеном? (y/n): ").lower()
        if response != 'y':
            sys.exit(1)
    
    # Варианты сохранения токена
    print("\nВыберите способ сохранения токена:")
    print("1. В переменную окружения (временно для текущей сессии)")
    print("2. В файл .env (рекомендуется)")
    print("3. В файл bot_config.py (как константу)")
    
    choice = input("Введите номер (1-3): ").strip()
    
    if choice == "1":
        # Устанавливаем как переменную окружения для текущей сессии
        os.environ["BOT_TOKEN"] = token
        print(f"\nТокен установлен как переменная окружения для текущей сессии.")
        print("Вы можете запустить бота командой: python bot.py")
        
    elif choice == "2":
        # Создаем файл .env
        env_content = f"BOT_TOKEN={token}\n"
        
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        
        print(f"\nТокен сохранен в файл .env")
        print("Для использования добавьте в .env файл вашей системы или запускайте:")
        print("source .env && python bot.py")
        
        # Добавляем .env в .gitignore, если он существует
        gitignore_path = Path(".gitignore")
        if gitignore_path.exists():
            with open(gitignore_path, "r", encoding="utf-8") as f:
                gitignore_content = f.read()
            
            if ".env" not in gitignore_content:
                with open(gitignore_path, "a", encoding="utf-8") as f:
                    f.write("\n.env\n")
                print("Файл .env добавлен в .gitignore для безопасности")
    
    elif choice == "3":
        # Создаем файл конфигурации
        config_content = f'''"""
Конфигурационный файл для Telegram-бота ProFileER
"""

# Токен Telegram-бота
BOT_TOKEN = "{token}"

# Другие настройки бота можно добавить здесь
'''
        
        with open("bot_config.py", "w", encoding="utf-8") as f:
            f.write(config_content)
        
        print(f"\nТокен сохранен в файл bot_config.py")
        print("Теперь нужно обновить bot.py, чтобы он использовал этот файл.")
        
        # Обновляем bot.py, чтобы использовать bot_config.py
        update_bot_file()
    
    else:
        print("Неверный выбор!")
        sys.exit(1)
    
    print(f"\nНастройка завершена! Вы можете запустить бота командой: python bot.py")


def update_bot_file():
    """Обновляем bot.py, чтобы использовать bot_config.py"""
    try:
        with open("bot.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Проверяем, что токен уже не определен через bot_config
        if 'from bot_config import BOT_TOKEN' not in content:
            # Заменяем строку импорта и получение токена
            if 'import os' in content and 'BOT_TOKEN = os.getenv("BOT_TOKEN")' in content:
                updated_content = content.replace(
                    'import os',
                    'import os\ntry:\n    from bot_config import BOT_TOKEN  # Импортируем токен из конфига\nexcept ImportError:\n    # Если файла bot_config.py нет, используем переменную окружения\n    BOT_TOKEN = os.getenv("BOT_TOKEN")'
                ).replace(
                    'BOT_TOKEN = os.getenv("BOT_TOKEN")',
                    '# Токен теперь импортируется из bot_config.py или переменной окружения'
                )
                
                with open("bot.py", "w", encoding="utf-8") as f:
                    f.write(updated_content)
                
                print("Файл bot.py обновлен для использования bot_config.py")
            else:
                print("Не удалось автоматически обновить bot.py, обновите его вручную")
        else:
            print("Файл bot.py уже обновлен для использования bot_config.py")
    except Exception as e:
        print(f"Ошибка при обновлении bot.py: {e}")


def show_usage():
    """Показать инструкцию по использованию"""
    print("\n" + "="*50)
    print("ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:")
    print("="*50)
    print("1. Убедитесь, что у вас установлены зависимости:")
    print("   pip install -r requirements.txt")
    print("\n2. Запустите бота командой:")
    print("   python bot.py")
    print("\n3. В Telegram найдите вашего бота и начните чат с команды /start")
    print("\n4. Используйте команды:")
    print("   /start - начать работу с ботом")
    print("   /profiles - получить список профилей")
    print("   /help - получить справочную информацию")


if __name__ == "__main__":
    setup_bot_token()
    show_usage()