import os
import json
from flask import Flask, render_template, request, jsonify

# Пытаемся импортировать из текущей директории, а если не получится - из родительской
try:
    from settings import DATA_FILE
    print(f"Используем настройки из локального импорта: DATA_FILE={DATA_FILE}")
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from settings import DATA_FILE
    print(f"Используем настройки из родительского импорта: DATA_FILE={DATA_FILE}")


def create_app():
    app = Flask(__name__)
    
    # Загрузка профилей
    def load_profiles():
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
                        profiles = json.load(f)
                        print(f"✓ УСПЕШНО: Загружено {len(profiles)} профилей из файла: {data_file_path}")
                        print(f"  Первые два профиля: {[p['name'] for p in profiles[:2]]}")
                        return profiles
                except json.JSONDecodeError as e:
                    print(f"✗ ОШИБКА: Неверный формат JSON в файле {data_file_path}: {e}")
                    continue
                except PermissionError:
                    print(f"✗ ОШИБКА: Нет доступа к файлу {data_file_path}")
                    continue
                except Exception as e:
                    print(f"✗ ОШИБКА: Не удалось открыть файл {data_file_path}: {str(e)}")
                    continue
            else:
                print(f"✗ ФАЙЛ НЕ НАЙДЕН: {data_file_path}")
        
        print("❌ Ни один из файлов профилей не найден или не может быть прочитан.")
        print("Используем встроенные примеры профилей...")
        
        # Возвращаем встроенные примеры
        default_profiles = [
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
                ],
                "deception_signs": [
                    "Отказ выполнять задачи как форма саботажа",
                    "Скрытая критика",
                    "Намеренные задержки",
                    "Ироничные замечания",
                    "Отказ общаться как форма наказания",
                    "Перекладывание вины на других"
                ],
                "dialog_recommendations": [
                    "Ясно и четко выражать ожидания",
                    "Избегать обвинительного тона",
                    "Документировать устные соглашения",
                    "Обсуждать поведение открыто",
                    "Поощрять прямое выражение недовольства",
                    "Фокусироваться на конкретных поведенческих актах"
                ]
            }
        ]
        
        print(f"Возвращаем {len(default_profiles)} встроенных профилей")
        return default_profiles

    @app.route('/')
    def index():
        profiles = load_profiles()
        return render_template('index.html', profiles=profiles)

    @app.route('/profile/<int:profile_id>')
    def profile_detail(profile_id):
        profiles = load_profiles()
        if profile_id < len(profiles):
            profile = profiles[profile_id]
            return render_template('profile_detail.html', profile=profile, profile_id=profile_id)
        else:
            return "Профиль не найден", 404

    @app.route('/api/profiles')
    def api_profiles():
        profiles = load_profiles()
        return jsonify(profiles)

    @app.route('/api/profile/<int:profile_id>')
    def api_profile_detail(profile_id):
        profiles = load_profiles()
        if profile_id < len(profiles):
            return jsonify(profiles[profile_id])
        else:
            return jsonify({"error": "Профиль не найден"}), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)