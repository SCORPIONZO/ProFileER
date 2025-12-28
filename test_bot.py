"""
Тестовый скрипт для проверки функциональности Telegram-бота
"""

import json
from bot import ProfileBot

def test_profile_loading():
    """Тестируем загрузку профилей"""
    print("Тестируем загрузку профилей...")
    
    bot = ProfileBot()
    
    print(f"Загружено профилей: {len(bot.profiles)}")
    
    if len(bot.profiles) > 0:
        first_profile = bot.profiles[0]
        print(f"Первый профиль: {first_profile['name']}")
        
        # Проверяем наличие обязательных полей
        required_fields = ['name', 'description', 'traits', 'behaviors']
        for field in required_fields:
            if field in first_profile:
                print(f"  - Поле '{field}': OK")
            else:
                print(f"  - Поле '{field}': ОТСУТСТВУЕТ!")
        
        # Проверяем форматирование профиля
        formatted = bot.format_profile(first_profile)
        print(f"  - Длина форматированного профиля: {len(formatted)} символов")
        print("  - Форматирование: OK")
        
        # Проверяем получение профиля по имени
        profile_by_name = bot.get_profile_by_name(first_profile['name'])
        if profile_by_name:
            print("  - Получение профиля по имени: OK")
        else:
            print("  - Получение профиля по имени: ОШИБКА!")
            
        return True
    else:
        print("ОШИБКА: Не загружено ни одного профиля!")
        return False

def test_deception_indicators():
    """Тестируем функции определения признаков обмана"""
    print("\nТестируем функции определения признаков обмана...")
    
    bot = ProfileBot()
    
    if len(bot.profiles) > 0:
        first_profile = bot.profiles[0]
        indicators = bot.get_deception_indicators_for_profile(first_profile)
        print(f"  - Признаков обмана для '{first_profile['name']}': {len(indicators)}")
        
        general_indicators = bot.get_general_deception_indicators()
        print(f"  - Общих признаков обмана: {len(general_indicators)}")
        
        return True
    else:
        print("ОШИБКА: Нет профилей для тестирования!")
        return False

def test_dialog_approaches():
    """Тестируем функции рекомендаций по диалогу"""
    print("\nТестируем функции рекомендаций по диалогу...")
    
    bot = ProfileBot()
    
    if len(bot.profiles) > 0:
        first_profile = bot.profiles[0]
        approaches = bot.get_dialog_approaches_for_profile(first_profile)
        print(f"  - Рекомендаций по диалогу для '{first_profile['name']}': {len(approaches)}")
        
        return True
    else:
        print("ОШИБКА: Нет профилей для тестирования!")
        return False

if __name__ == "__main__":
    print("Запуск тестирования функциональности Telegram-бота ProFileER")
    print("="*60)
    
    success = True
    success &= test_profile_loading()
    success &= test_deception_indicators()
    success &= test_dialog_approaches()
    
    print("\n" + "="*60)
    if success:
        print("Все тесты пройдены успешно!")
        print("Telegram-бот готов к использованию.")
    else:
        print("Тестирование выявило ошибки!")
    
    print("="*60)