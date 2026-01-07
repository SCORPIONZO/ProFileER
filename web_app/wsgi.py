#!/usr/bin/env python3
"""Application WSGI Entry Point."""

import sys
import os
from app import create_app

# Добавляем директорию в путь Python, чтобы можно было импортировать модули
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Создаем приложение Flask
app = create_app()

if __name__ == "__main__":
    # Запускаем приложение в режиме разработки только при прямом запуске этого файла
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))