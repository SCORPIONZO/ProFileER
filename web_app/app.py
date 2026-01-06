import os
import json
from flask import Flask, render_template, request, jsonify

# Пытаемся импортировать из текущей директории, а если не получится - из родительской
try:
    from settings import DATA_FILE
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from settings import DATA_FILE


def create_app():
    app = Flask(__name__)
    
    # Загрузка профилей
    def load_profiles():
        # Определяем возможные пути к файлу данных
        possible_paths = [
            # Текущая директория (web_app)
            os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_FILE),
            # Родительская директория (корень проекта)
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), DATA_FILE),
            # Абсолютный путь к файлу в корне проекта
            os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), DATA_FILE))
        ]
        
        for data_file_path in possible_paths:
            if os.path.exists(data_file_path):
                try:
                    with open(data_file_path, 'r', encoding='utf-8') as f:
                        profiles = json.load(f)
                        print(f"Загружено профилей: {len(profiles)} из файла: {data_file_path}")
                        return profiles
                except json.JSONDecodeError as e:
                    print(f"Ошибка чтения JSON из файла {data_file_path}: {e}")
                    continue
                except Exception as e:
                    print(f"Ошибка открытия файла {data_file_path}: {e}")
                    continue
        
        # Если ни один из файлов не найден или не может быть прочитан, возвращаем примеры
        print("Файл профилей не найден, используются встроенные примеры")
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