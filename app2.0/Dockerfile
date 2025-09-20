FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всех файлов приложения
COPY . .

# Создание необходимых директорий
RUN mkdir -p data uploads uploads/photos static/css static/js static/images templates backups

# Открытие порта
EXPOSE 5000

# Запуск приложения
CMD ["python", "app.py"]
