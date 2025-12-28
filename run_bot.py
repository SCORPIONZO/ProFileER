#!/usr/bin/env python3
"""
Скрипт для запуска Telegram-бота ProFileER
"""

import os
import sys
import subprocess

def run_bot():
    """Запуск Telegram-бота"""
    print("Запуск Telegram-бота ProFileER")
    print("="*50)
    
    # Проверяем, установлен ли токен в переменной окружения
    bot_token = os.getenv("BOT_TOKEN")
    
    if not bot_token:
        print("Токен бота не установлен как переменная окружения.")
        print("\033[91mВАЖНО: Если вы уже опубликовали токен где-либо (включая использование")
        print("в чатах с ИИ), вы ДОЛЖНЫ создать нового бота или сбросить токен старого,")
        print("так как опубликованный токен считается скомпрометированным.\033[0m")
        token_input = input("Введите токен бота (или нажмите Enter для выхода): ").strip()
        
        if not token_input:
            print("Токен не введен. Выход.")
            sys.exit(1)
        
        # Устанавливаем токен как переменную окружения для текущей сессии
        os.environ["BOT_TOKEN"] = token_input
        print("Токен установлен как переменная окружения для текущей сессии.")
    
    print("\nЗапускаем бота...")
    print("Для остановки бота нажмите Ctrl+C")
    print("-" * 40)
    
    try:
        # Запускаем бота как подпроцесс
        result = subprocess.run([sys.executable, "bot.py"], env=os.environ)
        
        if result.returncode == 0:
            print("\nБот успешно завершил работу.")
        else:
            print(f"\nБот завершил работу с кодом ошибки: {result.returncode}")
    
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем (Ctrl+C).")
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")

def check_dependencies():
    """Проверка установленных зависимостей"""
    print("Проверка зависимостей...")
    
    try:
        import telegram
        import json
        print("✓ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"✗ Не найдена зависимость: {e}")
        print("Установите зависимости командой: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    print("Telegram-бот ProFileER")
    print("Утилита запуска")
    print("="*50)
    
    if check_dependencies():
        run_bot()
    else:
        print("\nДля запуска бота необходимо установить зависимости.")
        install = input("Установить зависимости сейчас? (y/n): ").lower()
        if install == 'y':
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("Зависимости установлены. Перезапустите скрипт.")
        else:
            print("Установите зависимости вручную командой: pip install -r requirements.txt")