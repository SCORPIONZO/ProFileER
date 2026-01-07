import os
import sys
from app import create_app

# Получаем порт из переменной окружения, если он задан
port = int(os.environ.get("PORT", 5000))
host = os.environ.get("HOST", "0.0.0.0")

# Создаем приложение
app = create_app()

if __name__ == '__main__':
    print("Запуск ProFileER веб-приложения в режиме продакшн...")
    print(f"Сервер слушает {host}:{port}")
    
    app.run(
        debug=False,  # Отключаем режим отладки для продакшена
        host=host,
        port=port,
        threaded=True
    )