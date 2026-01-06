import os
import shutil
import sys
from pathlib import Path

def prepare_deployment():
    """Подготовка файлов для деплоя на Vercel"""
    # Получаем пути к директориям
    project_root = Path(__file__).parent.parent  # /Volumes/HDD/PYTHON/ProFileER
    web_app_dir = Path(__file__).parent         # /Volumes/HDD/PYTHON/ProFileER/web_app
    
    print(f"Корневая директория проекта: {project_root}")
    print(f"Директория web_app: {web_app_dir}")
    
    # Имя файла данных
    data_file = "profiles.json"
    
    # Определяем путь к исходному файлу (в web_app)
    source_path = web_app_dir / data_file
    
    if not source_path.exists():
        print(f"Файл {source_path} не найден!")
        return False
    
    print(f"Найден файл данных: {source_path}")
    
    # Копируем в корень проекта
    target_path = project_root / data_file
    try:
        shutil.copy2(source_path, target_path)
        print(f"Файл скопирован в корень проекта: {target_path}")
    except Exception as e:
        print(f"Ошибка при копировании в корень проекта: {e}")
        return False
    
    # Также копируем в текущую директорию web_app (на всякий случай)
    try:
        dest_path = web_app_dir / data_file
        shutil.copy2(source_path, dest_path)
        print(f"Файл скопирован в директорию web_app: {dest_path}")
    except Exception as e:
        print(f"Ошибка при копировании в web_app: {e}")
        return False
    
    # Проверяем количество профилей в каждом файле
    try:
        import json
        with open(source_path, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            print(f"Количество профилей в {source_path}: {len(profiles)}")
    except Exception as e:
        print(f"Ошибка при чтении {source_path}: {e}")
    
    try:
        import json
        with open(target_path, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            print(f"Количество профилей в {target_path}: {len(profiles)}")
    except Exception as e:
        print(f"Ошибка при чтении {target_path}: {e}")
    
    return True

if __name__ == "__main__":
    success = prepare_deployment()
    if success:
        print("Подготовка деплоя завершена успешно")
    else:
        print("Ошибка при подготовке деплоя")
        sys.exit(1)