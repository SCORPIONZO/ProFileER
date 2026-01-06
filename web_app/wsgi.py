import sys
import os

# Добавляем папку web_app в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Создаем приложение для Vercel
app = create_app()

# Vercel ожидает объект wsgi_app
wsgi_app = app

# Определяем application как точку входа для WSGI
application = wsgi_app