# Используем официальный образ Python
FROM python:3.8-slim

# Установка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Открытие порта
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "api/workout_api.py"]