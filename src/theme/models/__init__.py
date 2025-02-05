import os
import importlib

models_dir = os.path.dirname(__file__)

models = []

for filename in os.listdir(models_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"src.theme.models.{filename[:-3]}"  # Убираем .py
        # Импортируем модель
        importlib.import_module(module_name)
        # Добавляем имя модуля в список, используя правильный регистр
        models.append(filename[:-3].capitalize())  # Преобразуем в заглавные для __all__
__all__ = models
