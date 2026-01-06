from app import create_app

# Создаем приложение для Vercel
app = create_app()

# Vercel ожидает объект wsgi_app
wsgi_app = app