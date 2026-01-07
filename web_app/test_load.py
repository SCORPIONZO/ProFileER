import os
import sys
sys.path.append('..')  # Add parent directory to path to import settings

from settings import DATA_FILE

def load_profiles():
    """Copy of the same function used in app.py"""
    print("=== Начинаем поиск файла профилей ===")
    
    # Определяем возможные пути к файлу данных
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    possible_paths = [
        # Текущая директория (web_app)
        os.path.join(current_dir, DATA_FILE),
        # Родительская директория (корень проекта)
        os.path.join(parent_dir, DATA_FILE),
        # Путь в текущей директории (явно указываем)
        os.path.join(current_dir, 'profiles.json'),
        # Путь в родительской директории (явно указываем)
        os.path.join(parent_dir, 'profiles.json'),
        # Относительный путь от текущей директории
        os.path.join('..', DATA_FILE),
    ]
    
    print(f"Текущая директория: {current_dir}")
    print(f"Родительская директория: {parent_dir}")
    print(f"Ищем файл: {DATA_FILE}")
    
    for i, data_file_path in enumerate(possible_paths):
        print(f"Проверяем путь {i+1}: {data_file_path}")
        
        if os.path.exists(data_file_path):
            try:
                with open(data_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"Успешно загружено {len(data)} профилей из {data_file_path}")
                    return data
            except json.JSONDecodeError as e:
                print(f"Ошибка чтения JSON из {data_file_path}: {e}")
                continue
            except Exception as e:
                print(f"Ошибка при чтении {data_file_path}: {e}")
                continue
        else:
            print(f"Файл не найден")
    
    print("Файл профилей не найден, используем примеры")
    # Возвращаем примеры профилей, если файл не найден
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
            ],
            "deception_signs": [
                "Преувеличение своих достижений",
                "Использование харизмы для манипуляции",
                "Притворство в эмоциональных реакциях",
                "Игнорирование чужих чувств",
                "Попытки переманить сочувствие",
                "Показное благородство"
            ],
            "dialog_recommendations": [
                "Сохранять спокойствие и дистанцию",
                "Не поддаваться на манипуляции",
                "Устанавливать четкие границы",
                "Не вступать в эмоциональные дебаты",
                "Фокусироваться на фактах, а не на эмоциях",
                "Избегать конфронтации"
            ]
        }
    ]

# Import json module for the function
import json

# Run the test
profiles = load_profiles()
print(f"Total profiles loaded: {len(profiles)}")
if profiles:
    print(f"First profile: {profiles[0]['name']}")