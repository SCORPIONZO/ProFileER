import os
import sys
from app import create_app


def main():
    # Создаем приложение
    app = create_app()
    
    # Получаем порт из переменной окружения или используем 5000 по умолчанию
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"Запуск веб-приложения на {host}:{port}")
    print("Для остановки приложения нажмите Ctrl+C")
    
    # Запускаем приложение
    app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    main()